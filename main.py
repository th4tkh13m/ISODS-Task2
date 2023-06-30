from scraper.scraper import Scraper

if __name__ == "__main__":
    save_dir = "./images"
    scraper = Scraper()
    scraper.fetch_ai_images("man")
    scraper.fetch_true_images("man")
    scraper.save_ai_images(save_dir)
    scraper.save_true_images(save_dir)
    scraper.quit_driver()