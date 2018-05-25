import pstats
p = pstats.Stats('profile.txt')
p.strip_dirs().sort_stats("time").print_stats()
