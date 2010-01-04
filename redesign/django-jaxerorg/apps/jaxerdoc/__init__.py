try:
    import djapian
except:
    djapian = None
if djapian:    
    djapian.load_indexes()