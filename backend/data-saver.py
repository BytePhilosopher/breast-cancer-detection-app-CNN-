import os
import shutil

source_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../dataset/archive/'))  # Use absolute path
target_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../dataset'))

os.makedirs(os.path.join(target_dir, '0'), exist_ok=True)
os.makedirs(os.path.join(target_dir, '1'), exist_ok=True)

count = {'0': 0, '1': 0}

for patient_id in os.listdir(source_dir):
    patient_path = os.path.join(source_dir, patient_id)
    if not os.path.isdir(patient_path):
        continue

    for label in ['0', '1']:
        class_path = os.path.join(patient_path, label)
        if not os.path.isdir(class_path):
            continue

        for file in os.listdir(class_path):
            src = os.path.join(class_path, file)
            dst = os.path.join(target_dir, label, f"{label}_{count[label]}.png")
            shutil.copy2(src, dst)
            count[label] += 1

print(f"✅ Moved {count['0']} benign and {count['1']} malignant images to 'dataset/'")
