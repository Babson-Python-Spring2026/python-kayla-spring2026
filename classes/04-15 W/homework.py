def analyze_runs(nums):
    state = {
        "longest_increasing_run": 0,
        "longest_decreasing_run": 0,
        "num_increasing_runs": 0,
        "num_decreasing_runs": 0,
        "longest_increasing_values": [],
        "longest_decreasing_values": [],
        "longest_run_values": []
    }

    n = len(nums)
    if n < 2:
        return state

    current_run = [nums[0]]
    direction = None   # can be "inc", "dec", or None

    def finalize_run(run, run_direction):
        run_len = len(run)
        if run_direction is None or run_len < 2:
            return

        if run_direction == "inc":
            state["num_increasing_runs"] += 1

            if run_len > state["longest_increasing_run"]:
                state["longest_increasing_run"] = run_len
                state["longest_increasing_values"] = [run[:]]
            elif run_len == state["longest_increasing_run"]:
                state["longest_increasing_values"].append(run[:])

        elif run_direction == "dec":
            state["num_decreasing_runs"] += 1

            if run_len > state["longest_decreasing_run"]:
                state["longest_decreasing_run"] = run_len
                state["longest_decreasing_values"] = [run[:]]
            elif run_len == state["longest_decreasing_run"]:
                state["longest_decreasing_values"].append(run[:])

    for i in range(1, n):
        prev = nums[i - 1]
        curr = nums[i]

        if curr > prev:
            new_direction = "inc"
        elif curr < prev:
            new_direction = "dec"
        else:
            new_direction = None

        if new_direction is None:
            finalize_run(current_run, direction)
            current_run = [curr]
            direction = None

        elif direction is None:
            current_run.append(curr)
            direction = new_direction

        elif new_direction == direction:
            current_run.append(curr)

        else:
            finalize_run(current_run, direction)
            current_run = [prev, curr]
            direction = new_direction

    finalize_run(current_run, direction)

    inc_len = state["longest_increasing_run"]
    dec_len = state["longest_decreasing_run"]

    if inc_len > dec_len:
        state["longest_run_values"] = state["longest_increasing_values"][:]
    elif dec_len > inc_len:
        state["longest_run_values"] = state["longest_decreasing_values"][:]
    elif inc_len == dec_len and inc_len > 0:
        state["longest_run_values"] = (
            state["longest_increasing_values"] +
            state["longest_decreasing_values"]
        )

    return state