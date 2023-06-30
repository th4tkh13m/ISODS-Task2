import argparse
from scraper.scraper import Scraper

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Image Scraper')

    parser.add_argument('query', type=str, help='Query for image search')
    parser.add_argument('save_dir', type=str, help='Directory to save the images')

    args = parser.parse_args()

    query = args.query
    save_dir = args.save_dir

    # Create an instance of the Scraper
    scraper = Scraper()

    # Fetch AI and true images based on the query
    scraper.fetch_ai_images(query)
    scraper.fetch_true_images(query)

    # Save AI and true images to the specified directory
    scraper.save_ai_images(save_dir)
    scraper.save_true_images(save_dir)

    # Quit the driver
    scraper.quit_driver()