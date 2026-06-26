!pip install opencv-python
!pip install scikit-image
!pip install scipy
!pip install pandas
!pip install matplotlib
!pip install pillow
!pip install numpy

print("All requested libraries are installed.")

import cv2
import numpy as np
import matplotlib.pyplot as plt
from google.colab import files

print("Core modules imported successfully for image processing and input.")

from google.colab import files

uploaded = files.upload()

if uploaded:
    img_path = list(uploaded.keys())[0]
    print(f'Using user-selected file: "{img_path}"')

    img_bgr = cv2.imread(img_path)

    if img_bgr is None:
        print("Error: Could not read the image.")
    else:
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

        plt.figure(figsize=(10, 10))
        plt.imshow(img_rgb)
        plt.title('Uploaded Petri Dish Image')
        plt.axis('off')
        plt.show()

        num_disks = 2

        scaling_value = 6.0
        scaling_type = "Disk Diameter"

else:
    print("No file was uploaded.")

no_inhibition_margin_mm = 5.0 # @param {type:"number"}

concentricity_tolerance_factor = 1.5 # @param {type:"number"}

gray_img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

blurred_img = cv2.GaussianBlur(gray_img, (9, 9), 2)

img_height, img_width = gray_img.shape[:2]
min_petri_radius = int(min(img_height, img_width) * 0.3)
max_petri_radius = int(max(img_height, img_width) * 0.5)

petri_circles = cv2.HoughCircles(
    blurred_img,
    cv2.HOUGH_GRADIENT,
    dp=1,
    minDist=min_petri_radius,
    param1=50,
    param2=30,
    minRadius=min_petri_radius,
    maxRadius=max_petri_radius
)

petri_center = None
petri_radius = None
petri_dish_isolated = None

if petri_circles is not None:
    petri_circles = np.uint16(np.around(petri_circles))
    petri_circle = sorted(petri_circles[0, :], key=lambda x: x[2], reverse=True)[0]
    petri_center = (petri_circle[0], petri_circle[1])
    petri_radius = petri_circle[2]

    print(f"Detected Petri Dish: Center={petri_center}, Radius={petri_radius} pixels.")

    mask = np.zeros(img_bgr.shape[:2], dtype="uint8")
    cv2.circle(mask, petri_center, petri_radius, 255, -1)
    petri_dish_isolated = cv2.bitwise_and(img_bgr, img_bgr, mask=mask)

    display_petri_dish = img_rgb.copy()
    cv2.circle(display_petri_dish, petri_center, petri_radius, (0, 255, 0), 3)
    plt.figure(figsize=(10, 10))
    plt.imshow(display_petri_dish)
    plt.title('Detected Petri Dish')
    plt.axis('off')
    plt.show()

else:
    print("Error: Could not detect petri dish. Please adjust parameters or check image quality.")

if 'petri_dish_isolated' not in locals():
    print("Error: 'petri_dish_isolated' not found. Please ensure the 'Petri Dish Detection' cell was run successfully.")
else:
    gray_petri = cv2.cvtColor(petri_dish_isolated, cv2.COLOR_BGR2GRAY)

    blurred_petri = cv2.medianBlur(gray_petri, 5)

    min_disk_radius = int(petri_radius * 0.05)
    max_disk_radius = int(petri_radius * 0.20)

    print(f"Attempting to detect disks with radius between {min_disk_radius} and {max_disk_radius} pixels.")

    circles = cv2.HoughCircles(
        blurred_petri,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=min_disk_radius * 2,
        param2=30,
        minRadius=min_disk_radius,
        maxRadius=max_disk_radius
    )

    detected_disks = []
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center_x, center_y, radius = i[0], i[1], i[2]

            distance_from_petri_center = np.sqrt((center_x - petri_center[0])**2 + (center_y - petri_center[1])**2)
            if distance_from_petri_center + radius < petri_radius:
                detected_disks.append((center_x, center_y, radius))

        if len(detected_disks) > num_disks:
            print(f"Warning: Detected {len(detected_disks)} potential disks, but expected {num_disks}. Taking the first {num_disks}.")
            detected_disks = detected_disks[:num_disks]
        elif len(detected_disks) < num_disks:
            print(f"Warning: Detected only {len(detected_disks)} disks, but expected {num_disks}. Proceeding with detected disks.")


    display_img_with_disks = img_rgb.copy()

    cv2.circle(display_img_with_disks, petri_center, petri_radius, (0, 0, 255), 3)

    if detected_disks:
        print(f"Found {len(detected_disks)} disks.")
        for idx, (x, y, r) in enumerate(detected_disks):
            cv2.circle(display_img_with_disks, (x, y), r, (0, 255, 0), 3)
            cv2.circle(display_img_with_disks, (x, y), 2, (255, 0, 0), -1)
            cv2.putText(display_img_with_disks, str(idx+1), (x + 10, y + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        plt.figure(figsize=(10, 10))
        plt.imshow(display_img_with_disks)
        plt.title('Detected Disks in Petri Dish')
        plt.axis('off')
        plt.show()

    else:
        print("No disks detected. You may need to adjust Hough Circle parameters (minRadius, maxRadius, param1, param2, minDist).")

if detected_disks:
    avg_detected_disk_radius_pixels = np.mean([d[2] for d in detected_disks])
    avg_detected_disk_diameter_pixels = avg_detected_disk_radius_pixels * 2

    if scaling_value > 0:
        pixels_per_mm = avg_detected_disk_diameter_pixels / scaling_value
        print(f"Calculated scaling factor: {pixels_per_mm:.2f} pixels/mm")
    else:
        pixels_per_mm = None
        print("Error: Scaling value must be greater than 0.")
else:
    pixels_per_mm = None
    print("Error: No disks detected to calculate scaling factor.")

no_inhibition_threshold_mm = scaling_value + no_inhibition_margin_mm
print(f"No inhibition threshold set to: {no_inhibition_threshold_mm} mm (Disk Diameter + Margin)")

inhibition_zone_results = []

print("Starting inhibition zone diameter measurement with radial intensity profile analysis...")

img_lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)

for idx, (disk_cx, disk_cy, disk_r) in enumerate(detected_disks):
    radial_boundary_distances = []
    num_angles = 180
    step_angle = 2

    petri_center_x_int = int(petri_center[0])
    petri_center_y_int = int(petri_center[1])

    for angle_step in range(num_angles):
        angle_deg = angle_step * step_angle
        angle_rad = np.deg2rad(angle_deg)
        max_search_distance = petri_radius

        l_profile_values = []
        distances_along_radial = []
        current_distance = disk_r + 5

        while current_distance < max_search_distance:
            px = int(disk_cx + current_distance * np.cos(angle_rad))
            py = int(disk_cy + current_distance * np.sin(angle_rad))

            if not (0 <= px < img_lab.shape[1] and 0 <= py < img_lab.shape[0]):
                break

            dist_from_petri_center = np.sqrt((px - petri_center_x_int)**2 + (py - petri_center_y_int)**2)
            if dist_from_petri_center >= petri_radius - 2:
                break

            l_value = img_lab[py, px, 0]
            l_profile_values.append(l_value)
            distances_along_radial.append(current_distance)

            current_distance += 1

        if len(l_profile_values) > 10:
            l_profile_array = np.array(l_profile_values)
            radial_dist_array = np.array(distances_along_radial)

            window_size_smoothing = 5
            if len(l_profile_array) >= window_size_smoothing:
                l_profile_smoothed = np.convolve(l_profile_array, np.ones(window_size_smoothing)/window_size_smoothing, mode='valid')
                radial_dist_smoothed = radial_dist_array[window_size_smoothing-1:]

                window_size_plateau = 7
                found_plateau_start_idx = -1

                for i in range(len(l_profile_smoothed) - window_size_plateau + 1):
                    current_plateau_window_l = l_profile_smoothed[i:i+window_size_plateau]

                    if np.mean(current_plateau_window_l) > 100 and np.std(current_plateau_window_l) < 15:
                        found_plateau_start_idx = i
                        break

                if found_plateau_start_idx != -1:
                    radial_boundary_distances.append(radial_dist_smoothed[found_plateau_start_idx])

    if radial_boundary_distances:
        avg_inhibition_radius = np.mean(radial_boundary_distances)
        inhibition_zone_diameter_pixels = avg_inhibition_radius * 2

        if pixels_per_mm is not None and pixels_per_mm > 0:
            inhibition_diam_mm = inhibition_zone_diameter_pixels / pixels_per_mm
        else:
            inhibition_diam_mm = None

        ellipse_params = None

        contour_points = []
        for i, dist in enumerate(radial_boundary_distances):
            angle_deg = i * step_angle
            angle_rad = np.deg2rad(angle_deg)
            px = int(disk_cx + dist * np.cos(angle_rad))
            py = int(disk_cy + dist * np.sin(angle_rad))
            contour_points.append([px, py])

        if len(contour_points) >= 5:
            contour_points_np = np.array(contour_points, dtype=np.int32)
            ellipse = cv2.fitEllipse(contour_points_np)
            ellipse_params = ellipse
            print(f"Disk {idx+1}: Inhibition zone visualized as an ellipse.")
        else:
            print(f"Disk {idx+1}: Inhibition zone visualized as a circle (not enough points for ellipse).")

        print(f"Disk {idx+1}: Average Inhibition Zone Diameter (pixels): {inhibition_zone_diameter_pixels:.2f}")
        inhibition_zone_results.append({
            'Disk_ID': idx + 1,
            'Inhibition_Diameter_pixels': inhibition_zone_diameter_pixels,
            'Detected_Disk_Radius_pixels': disk_r,
            'Ellipse_Params': ellipse_params
        })
    else:
        print(f"Disk {idx+1}: Inhibition zone boundary could not be determined for any angle.")
        inhibition_zone_results.append({
            'Disk_ID': idx + 1,
            'Inhibition_Diameter_pixels': "Not Found",
            'Detected_Disk_Radius_pixels': disk_r,
            'Ellipse_Params': None
        })

import math

final_inhibition_measurements = []

for result in inhibition_zone_results:
    disk_id = int(result['Disk_ID'])
    inhibition_diam_pixels = result['Inhibition_Diameter_pixels']
    detected_disk_radius_pixels = int(result['Detected_Disk_Radius_pixels'])
    ellipse_params = result['Ellipse_Params']

    processed_result = {
        'Disk_ID': disk_id,
        'Inhibition_Diameter_pixels': (float(inhibition_diam_pixels) if isinstance(inhibition_diam_pixels, (np.floating, np.integer)) else inhibition_diam_pixels),
        'Detected_Disk_Radius_pixels': detected_disk_radius_pixels,
        'Status': 'Valid'
    }

    if inhibition_diam_pixels == "Çap Bulunamadı" or inhibition_diam_pixels == "Not Found" or pixels_per_mm is None:
        processed_result.update({
            'Inhibition_Diameter_mm': "Çap Yok",
            'Inhibition_Radius_mm': "Çap Yok",
            'Min_Inhibition_Radius_mm': "Çap Yok",
            'Max_Inhibition_Radius_mm': "Çap Yok",
            'Status': 'No Inhibition' if inhibition_diam_pixels == "Çap Bulunamadı" else 'No Detection'
        })
    else:
        inhibition_diam_mm = float(inhibition_diam_pixels / pixels_per_mm)
        inhibition_zone_radius_mm = inhibition_diam_mm / 2.0

        processed_result['Inhibition_Diameter_mm'] = round(inhibition_diam_mm, 2)
        processed_result['Inhibition_Radius_mm'] = round(inhibition_zone_radius_mm, 2)

        if inhibition_diam_mm <= no_inhibition_threshold_mm:
             processed_result.update({
                'Inhibition_Diameter_mm': "Çap Yok",
                'Inhibition_Radius_mm': "Çap Yok",
                'Min_Inhibition_Radius_mm': "Çap Yok",
                'Max_Inhibition_Radius_mm': "Çap Yok",
                'Status': 'No Inhibition (Threshold)'
            })
        else:
            if ellipse_params:
                ((ellipse_cx, ellipse_cy), (minor_axis_pixels, major_axis_pixels), angle) = ellipse_params
                disk_cx, disk_cy, disk_r = detected_disks[disk_id - 1] # Assuming detected_disks is indexed from 0

                distance = math.sqrt((disk_cx - ellipse_cx)**2 + (disk_cy - ellipse_cy)**2)

                disk_r_float = float(disk_r)

                concentricity_tolerance_pixels = disk_r_float * concentricity_tolerance_factor

                if distance > concentricity_tolerance_pixels:
                    processed_result.update({
                        'Inhibition_Diameter_mm': "Çap Yok",
                        'Inhibition_Radius_mm': "Çap Yok",
                        'Min_Inhibition_Radius_mm': "Çap Yok",
                        'Max_Inhibition_Radius_mm': "Çap Yok",
                        'Status': 'No Inhibition (Concentricity)'
                    })
                    print(f"Disk {disk_id}: Çap Bulunamadı.")
                else:
                    if minor_axis_pixels > major_axis_pixels:
                        minor_axis_pixels, major_axis_pixels = major_axis_pixels, minor_axis_pixels

                    major_radius_mm = round(float(major_axis_pixels) / pixels_per_mm / 2, 2)
                    minor_radius_mm = round(float(minor_axis_pixels) / pixels_per_mm / 2, 2)

                    processed_result.update({
                        'Major_Axis_mm': round(float(major_axis_pixels) / pixels_per_mm, 2),
                        'Minor_Axis_mm': round(float(minor_axis_pixels) / pixels_per_mm, 2),
                        'Min_Inhibition_Radius_mm': minor_radius_mm,
                        'Max_Inhibition_Radius_mm': major_radius_mm
                    })
            else:
                circle_radius_mm = round(inhibition_diam_mm / 2, 2)

                processed_result.update({
                    'Major_Axis_mm': round(inhibition_diam_mm, 2),
                    'Minor_Axis_mm': round(inhibition_diam_mm, 2),
                    'Min_Inhibition_Radius_mm': circle_radius_mm,
                    'Max_Inhibition_Radius_mm': circle_radius_mm
                })

    final_inhibition_measurements.append(processed_result)

print("Inhibition zone measurements processed.")

display_img_final = img_rgb.copy()

cv2.circle(display_img_final, petri_center, petri_radius, (0, 0, 255), 3)

if 'detected_disks' in locals() and detected_disks:
    for idx, (x, y, r) in enumerate(detected_disks):
        cv2.circle(display_img_final, (x, y), r, (0, 255, 0), 3)
        cv2.circle(display_img_final, (x, y), 2, (255, 0, 0), -1)

for result in final_inhibition_measurements:
    if result['Status'] == 'Valid':
        disk_id = result['Disk_ID']
        disk_cx, disk_cy, disk_r = detected_disks[disk_id - 1]

        original_inhibition_result = next(item for item in inhibition_zone_results if item["Disk_ID"] == disk_id)

        ellipse_params = original_inhibition_result.get('Ellipse_Params')
        inhibition_diam_pixels = original_inhibition_result['Inhibition_Diameter_pixels']

        if ellipse_params:
            cv2.ellipse(display_img_final, ellipse_params, (150, 0, 0), 2)
            print(f"Disk {disk_id}: Valid inhibition zone visualized as an ellipse.")
        elif isinstance(inhibition_diam_pixels, (np.floating, np.integer)):
            avg_inhibition_radius = inhibition_diam_pixels / 2
            cv2.circle(display_img_final, (disk_cx, disk_cy), int(avg_inhibition_radius), (150, 0, 0), 2) # Dark blue (BGR)
            print(f"Disk {disk_id}: Valid inhibition zone visualized as a circle.")

plt.figure(figsize=(12, 12))
plt.imshow(display_img_final)
plt.title('Detected Disks and Valid Inhibition Zones')
plt.axis('off')
plt.show()

import pandas as pd
import json
from IPython.display import display

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

df_measurements = pd.DataFrame(final_inhibition_measurements)

print("Inhibition Zone Diameter and Radii (mm):")
display_columns = ['Disk_ID', 'Inhibition_Diameter_mm', 'Min_Inhibition_Radius_mm', 'Max_Inhibition_Radius_mm']
display(df_measurements[display_columns])

filtered_json_output = []
for item in final_inhibition_measurements:
    filtered_item = {
        'Disk_ID': item['Disk_ID'],
        'Inhibition_Diameter_mm': item['Inhibition_Diameter_mm'],
        'Min_Inhibition_Radius_mm': item['Min_Inhibition_Radius_mm'],
        'Max_Inhibition_Radius_mm': item['Max_Inhibition_Radius_mm']
    }
    filtered_json_output.append(filtered_item)

json_measurements = json.dumps(filtered_json_output, indent=4, ensure_ascii=False)

print(json_measurements)