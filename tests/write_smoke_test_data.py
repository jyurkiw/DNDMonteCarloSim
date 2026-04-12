from dndmontecarlosim.sim_plan import get_simulation_plan_template
from dndmontecarlosim.runner import run, save

if __name__ == "__main__":
    import os
    print(os.path.abspath("."))
    simplan = get_simulation_plan_template()
    data = run("Test Plan 01", simplan)
    print(data)
    save(data, f"tests/runner_output/Test_Plan_01.csv")
