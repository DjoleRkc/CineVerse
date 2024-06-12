# Autor: Đorđe Pajić
import os
from django.core.management.base import BaseCommand
from PIL import Image


class Command(BaseCommand):
    """
        Django management command to resize images for carousel.

        This command resizes images found in a specified folder to the desired width and height.

        Args:
            folder_path (str): The path to the folder containing the original images.
            output_folder (str): The path to the folder where resized images will be saved.
            width (int): The desired width of the resized images.
            height (int): The desired height of the resized images.
    """

    help = 'Resize svih slika za carousel'

    def add_arguments(self, parser):
        """
                Adds command line arguments for the management command.

                Args:
                    parser: The argument parser.
        """
        parser.add_argument('folder_path', type=str, help='Path do foldera sa slikama')
        parser.add_argument('output_folder', type=str,
                            help='Path do foldera gde ce biti smestene resizovane slike (nama je to isti folder u kom se vec nalaze)')
        parser.add_argument('width', type=int, help='Zeljena sirina slika')
        parser.add_argument('height', type=int, help='Zeljena visina slika')

    def handle(self, **options):
        """
                Executes the resizing operation.

                Args:
                    **options: Command line options.

                Returns:
                    None
        """
        folder_path = options['folder_path']
        output_folder = options['output_folder']
        width = options['width']
        height = options['height']

        for filename in os.listdir(folder_path):
            filepath = os.path.join(folder_path, filename)
            if os.path.isfile(filepath):
                try:
                    img = Image.open(filepath)
                    img.thumbnail((width, height))
                    img.save(os.path.join(output_folder, filename))
                    self.stdout.write(self.style.SUCCESS(f"Resized {filename} successfully."))
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f"Error resizing {filename}: {e}"))

# runuje se sa python manage.py resize_images <folder_path> <output_folder> <width> <height>