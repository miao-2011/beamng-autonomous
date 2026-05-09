from beamngpy import BeamNGpy, Scenario, Vehicle
from beamngpy.sensors import Camera
import os

def main():
    # Connect to local BeamNG instance
    bng = BeamNGpy("localhost", 25252)
    bng.open()

    # Create scenario on Italy map
    scenario = Scenario("italy", "autonomous_driving")

    # Create vehicle
    ego = Vehicle("ego_vehicle", model="etk800", color="White")
    scenario.add_vehicle(
        ego,
        pos=(237.90, -894.42, 246.10),
        rot_quat=(0.0173, -0.0019, -0.6354, 0.7720)
    )

    # Compile and start scenario
    scenario.make(bng)
    bng.settings.set_deterministic(60)
    bng.control.pause()
    bng.scenario.load(scenario)
    bng.scenario.start()

    # Enable built-in AI traffic mode
    ego.ai.set_mode("traffic")

    # Front camera
    cam_front = Camera(
        "front_cam", bng, ego,
        requested_update_time=0.01,
        is_using_shared_memory=True,
        pos=(-0.3, 1, 2),
        dir=(0, -1, 0),
        field_of_view_y=70,
        near_far_planes=(0.1, 1000),
        resolution=(512, 512),
        is_streaming=True,
        is_render_annotations=True
    )

    # Rear camera
    cam_rear = Camera(
        "rear_cam", bng, ego,
        requested_update_time=0.01,
        is_using_shared_memory=True,
        pos=(0, -1.5, 1.0),
        dir=(0, 1, 0),
        field_of_view_y=70,
        near_far_planes=(0.1, 1000),
        resolution=(512, 512),
        is_streaming=True
    )

    # Prepare output directory
    output_dir = "captures"
    os.makedirs(output_dir, exist_ok=True)

    step = 0
    print("Autonomous driving running...")

    try:
        while True:
            bng.control.step(10)
            step += 1

            # Save frames periodically
            if step % 10 == 0:
                front = cam_front.stream()
                rear = cam_rear.stream()

                front["colour"].save(f"{output_dir}/front_{step}.png")
                rear["colour"].save(f"{output_dir}/rear_{step}.png")

    except KeyboardInterrupt:
        print("\nStopped.")

    # Cleanup
    bng.control.resume()
    bng.disconnect()

if __name__ == "__main__":
    main()
