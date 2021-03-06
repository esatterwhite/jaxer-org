from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.daemonize import become_daemon
from django.contrib.contenttypes.models import ContentType

import os
import sys
import operator
from datetime import datetime
from optparse import make_option

from djapian.models import Change
from djapian import utils
from djapian.utils.paging import paginate
from djapian.utils.commiter import Commiter
from djapian import IndexSpace

def get_content_types(*actions):
    types = Change.objects.filter(action__in=actions)\
                    .values_list('content_type', flat=True)\
                    .distinct()
    return ContentType.objects.filter(pk__in=types)

def get_indexers(content_type):
    return reduce(
        operator.add,
        [space.get_indexers_for_model(content_type.model_class())
            for space in IndexSpace.instances]
    )

@transaction.commit_manually
def update_changes(verbose, timeout, once, per_page, commit_each):
    counter = [0]

    def reset_counter():
        counter[0] = [0]

    def after_index(obj):
        counter[0] += 1

        if verbose:
            sys.stdout.write('.')
            sys.stdout.flush()

    commiter = Commiter.create(commit_each)(
        lambda: None,
        transaction.commit,
        transaction.rollback
    )

    while True:
        count = Change.objects.count()
        if count > 0 and verbose:
            print 'There are %d objects to update' % count

        for ct in get_content_types('add', 'update'):
            indexers = get_indexers(ct)

            for page in paginate(
                            Change.objects.filter(content_type=ct, action__in=('add', 'update'))\
                                .select_related('content_type')\
                                .order_by('object_id'),
                            per_page
                        ):# The objects must be sorted by date
                commiter.begin_page()

                try:
                    for indexer in indexers:
                        indexer.update(
                            ct.model_class()._default_manager.filter(
                                pk__in=[c.object_id for c in page.object_list]
                            ).order_by('pk'),
                            after_index,
                            per_page,
                            commit_each
                        )

                    for change in page.object_list:
                        change.delete()

                    commiter.commit_page()
                except Exception:
                    if commit_each:
                        for change in page.object_list[:counter[0]]:
                            change.delete()
                        commiter.commit_object()
                    else:
                        commiter.cancel_page()
                    raise

                reset_counter()

        for ct in get_content_types('delete'):
            indexers = get_indexers(ct)

            for change in Change.objects.filter(content_type=ct, action='delete'):
                for indexer in indexers:
                    indexer.delete(change.object_id)
                    change.delete()

        if once:
            break

        time.sleep(timeout)

def rebuild(verbose, per_page, commit_each):
    def after_index(obj):
        if verbose:
            sys.stdout.write('.')
            sys.stdout.flush()

    for space in IndexSpace.instances:
        for model, indexers in space.get_indexers().iteritems():
            for indexer in indexers:
                indexer.clear()
                indexer.update(None, after_index, per_page, commit_each)

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--verbose', action='store_true', default=False,
                    help='Verbosity output'),
        make_option('--daemonize', dest='make_daemon', default=False,
                    action='store_true',
                    help='Do not fork the process'),
        make_option('--time-out', dest='timeout', default=10, type='int',
                    help='Time to sleep between each query to the'
                         ' database (default: %default)'),
        make_option('--rebuild', dest='rebuild_index', default=False,
                    action='store_true',
                    help='Rebuild index database'),
        make_option('--per_page', dest='per_page', default=1000,
                    action='store', type=int,
                    help='Working page size'),
        make_option('--commit_each', dest='commit_each', default=False,
                    action='store_true',
                    help='Commit/flush changes on every document update'),
    )
    help = 'This is the Djapian daemon used to update the index based on djapian_change table.'

    requires_model_validation = True

    def handle(self, verbose=False, make_daemon=False, timeout=10,
               rebuild_index=False, per_page=1000, commit_each=False,
               *args, **options):
        utils.load_indexes()

        if make_daemon:
            become_daemon()

        if rebuild_index:
            rebuild(verbose, per_page, commit_each)
        else:
            update_changes(verbose, timeout, not make_daemon, per_page, commit_each)

        if verbose:
            print '\n'
