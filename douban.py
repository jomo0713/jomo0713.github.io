image_save_folder = 'static/images/douban/'
json_movie_path = 'data/douban/movie.json'
json_book_path = 'data/douban/book.json'
movie_status = {
    "mark": "想看",
    "doing": "在看",
    "done": "看过",
}
@retry(stop_max_attempt_number=3, wait_fixed=5000)
def fetch_subjects(user, type_, status):
    offset = 0
    page = 0
    url = f"https://{DOUBAN_API_HOST}/api/v2/user/{user}/interests"
    total = 0
    results = []
    /** 调用豆瓣接口获取数据 **/


def downloadImgs(image_url, id):
    # 确保文件夹路径存在
    os.makedirs(image_save_folder, exist_ok=True)
    file_name = "{id}.jpg".format(id=id)
    save_path = os.path.join(image_save_folder, file_name)

def insert_movie():
    results = []
    for i in movie_status.keys():
        results.extend(fetch_subjects(douban_name, "movie", i))
    # 确保文件的父目录存在
    os.makedirs(os.path.dirname(json_movie_path), exist_ok=True)
    # 检查文件是否存在
    if not os.path.exists(json_movie_path):
        # 文件不存在时，创建文件
        open(json_movie_path, 'w').close()  # 创建一个空文件
        print("File created.")
    json_data = []
    for item in results:
        # 下载图片文件
        downloadImgs(item["subject"]["pic"]["large"], item["id"])
        # 准备要追加的数据
        new_data = {}
        json_data.append(new_data)

    with open(json_movie_path, mode='w', newline='', encoding='utf-8') as file:
        json.dump(json_data, file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    douban_name = os.getenv('DOUBAN_NAME')
    if not douban_name:
        print('Douban name is not set')
        sys.exit(1)
    else:
        print(f"DOUBAN_NAME = {douban_name}")    
    insert_movie()

