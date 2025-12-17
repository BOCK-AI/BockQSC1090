def align_to_hardware_clock(schedule, clock=1e-9):
    for sp in schedule:
        sp.start_time = round(sp.start_time / clock) * clock
        sp.end_time = round(sp.end_time / clock) * clock
    return schedule
