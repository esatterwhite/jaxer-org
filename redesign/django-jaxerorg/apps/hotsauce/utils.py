from diff_match_patch.diff_match_patch import diff_match_patch


def make_difPatch(new_text, old_text):
    _dmp = diff_match_patch()
    '''returns the differenct between two strings as a string for storage in DB'''
    patch = _dmp.patch_make(new_text, old_text)
    return _dmp.patch_toText(patch)
