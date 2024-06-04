import cv2
import mediapipe as mp
from django.core.management.base import BaseCommand

mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=1)
drawSpec = mpDraw.DrawingSpec(thickness=1, circle_radius=1)

LEFT_EYEL_INDICES = {'left_eyel': [441, 442, 443, 444, 259, 257, 258, 286]}
FACE_TONE_INDICES = {'face_tone': [108, 109, 10, 338, 337, 151]}
UPPER_LIP_INDICES = {
    'upper_lip': [61, 191, 80, 81, 82, 13, 312, 311, 310, 415, 291, 409, 270, 269, 267, 0, 37, 39, 40, 185]}

class Neuro(BaseCommand):
    def neuro(self, image_paths):
        list_colors_photos = []
        for image_path in image_paths:
            img = cv2.imread(f"{image_path}")
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = faceMesh.process(imgRGB)

            if results.multi_face_landmarks:
                color_photos = {}
                for faceLms in results.multi_face_landmarks:
                    avarage_color = {}
                    mpDraw.draw_landmarks(img, faceLms, mpFaceMesh.FACEMESH_CONTOURS, drawSpec, drawSpec)
                    for id, lm in enumerate(faceLms.landmark):
                        ih, iw, ic = img.shape
                        x, y = int(lm.x * iw), int(lm.y * ih)

                        if id in list(LEFT_EYEL_INDICES.values())[0]:
                            cv2.circle(img, (x, y), 5, (255, 0, 0), -1)
                            roi = img[y:y + ih, x:x + iw]
                            average_raw = cv2.mean(roi)[::-1]
                            average = (int(average_raw[1]), int(average_raw[2]), int(average_raw[3]))
                            avarage_color[list(LEFT_EYEL_INDICES.keys())[0]] = average

                        elif id in list(FACE_TONE_INDICES.values())[0]:
                            cv2.circle(img, (x, y), 5, (255, 0, 0), -1)
                            roi = img[y:y + ih, x:x + iw]
                            average_raw = cv2.mean(roi)[::-1]
                            average = (int(average_raw[1]), int(average_raw[2]), int(average_raw[3]))
                            avarage_color[list(FACE_TONE_INDICES.keys())[0]] = average

                        elif id in list(UPPER_LIP_INDICES.values())[0]:
                            cv2.circle(img, (x, y), 5, (255, 0, 0), -1)
                            roi = img[y:y + ih, x:x + iw]
                            average_raw = cv2.mean(roi)[::-1]
                            average = (int(average_raw[1]), int(average_raw[2]), int(average_raw[3]))
                            avarage_color[list(UPPER_LIP_INDICES.keys())[0]] = average

                    color_photos[image_path] = avarage_color
            list_colors_photos.append(color_photos)
        return list_colors_photos
