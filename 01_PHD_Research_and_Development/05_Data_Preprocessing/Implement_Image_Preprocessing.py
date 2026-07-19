import os
import cv2


class Imageprocessing:

    def __init__(self, inp_dir, out_dir):
        self.inp_dir = inp_dir
        self.out_dir = out_dir


    # Read image
    def read_image(self, image_path):

        img = cv2.imread(image_path)

        if img is None:
            print("Image not found:", image_path)

        return img



    # Main image processing function
    def process_image(self, inp_path, save_base_path):

        img = self.read_image(inp_path)
        if img is None:
            return

        img_name = os.path.basename(inp_path)

        # 01 Resize
        resize_img = self.resize_img(img)
        resize_path = os.path.join(save_base_path, "01_resize", img_name)
        self.save_image(resize_img, resize_path)

        # 02 Noise Removal
        noise_img = self.noise_removal_img(resize_img)
        noise_path = os.path.join(save_base_path, "02_noise_removal", img_name)
        self.save_image(noise_img, noise_path)

        # 03 Contrast Enhancement
        contrast_img = self.contrast_enhancement(noise_img)
        contrast_path = os.path.join(save_base_path, "03_contrast_enhancement", img_name)
        self.save_image(contrast_img, contrast_path)


    # Resize
    def resize_img(self, img):
        return cv2.resize(img,(224,224))



    # Noise removal
    def noise_removal_img(self, img):
        return cv2.GaussianBlur(img, (5,5),0)

    # Contrast enhancement
    def contrast_enhancement(self, img):

        lab = cv2.cvtColor(img,cv2.COLOR_BGR2LAB)
        l,a,b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        l = clahe.apply(l)
        output = cv2.merge((l,a,b))
        output = cv2.cvtColor(output, cv2.COLOR_LAB2BGR)

        return output


    # Save image
    def save_image(self, img, save_path):

        folder = os.path.dirname(save_path)
        os.makedirs(folder, exist_ok=True)
        cv2.imwrite( save_path, img)
        print("Saved:", save_path)



    # Folder processing
    def process_folder(self):

        for category in os.listdir(self.inp_dir):
            category_path = os.path.join(self.inp_dir,category)

            if os.path.isdideveloper(category_path):
                for class_name in os.listdir(category_path):
                    class_path = os.path.join(category_path, class_name)

                    if os.path.isdir(class_path):
                        for img_name in os.listdir(class_path):
                            if img_name.lower().endswith((".jpg",".jpeg",".png")):

                                inp_path = os.path.join(class_path,img_name)
                                save_path = os.path.join(self.out_dir, category, class_name)
                                self.process_image(inp_path, save_path)


# Folder wise testing
processor = Imageprocessing("dataset","Output")
processor.process_folder()


# Single Image testing
processor = Imageprocessing("","Single_Output")
processor.process_image("test.jpg","Single_Output")