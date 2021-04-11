# --------------------- #
#     Profile Code      #
# --------------------- #
from core.fever_monitor import FeverMonitor

if __name__ == "__main__":
    # import profiling modules
    import pstats
    import cProfile

    # instantiate and enable the profiler
    pr = cProfile.Profile()
    pr.enable()

    # run inference
    fever_monitor = FeverMonitor(
        temp_threshold=38.0,
        temp_unit="Celsius",
        colormap_index=5,
        yolo_model="Standard",
        confidence_threshold=0.5,
        use_gpu=False)
    for i in range(100):
        fever_monitor.run()

    # disable the profiler
    pr.disable()

    # output the results statistics
    stats = pstats.Stats(pr).sort_stats('cumtime')
    stats.print_stats()