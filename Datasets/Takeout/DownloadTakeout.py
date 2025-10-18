import kagglehub
import shutil
import os

# Download latest version
path = kagglehub.dataset_download("henslersoftware/19560-indian-takeaway-orders")

# Define target folder
target_dir = "Datasets/Original"

# Create target directory if it doesn't exist
os.makedirs(target_dir, exist_ok=True)

# Copy all downloaded files to target_dir
for filename in os.listdir(path):
    src = os.path.join(path, filename)
    dst = os.path.join(target_dir, filename)
    if os.path.isfile(src):
        shutil.copy2(src, dst)

print("Dataset saved to:", os.path.abspath(target_dir))
