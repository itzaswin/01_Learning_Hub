import os


def process_folder(self):
    for category in os.listdir(self.inp_dir):
        category_path = os.path.join(self.inp_dir, category)

        if os.path.isdir(category_path):
            for class_name in os.listdir(category_path):
                class_path = os.path.join(category_path, class_name)

                if os.path.isdir(class_path):
                    for img_name in os.listdir(class_path):
                        if img_name.lower().endswith((".jpg", ".jpeg", ".png")):
                            inp_path = os.path.join(class_path, img_name)
                            save_path = os.path.join(self.out_dir, category, class_name)
                            self.process_image(inp_path, save_path)