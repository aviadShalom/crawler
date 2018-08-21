from flask import Flask,request
from flask import jsonify

import crawler

app = Flask(__name__)
app.secret_key = '11111111'



@app.route('/ExtractInfoFromWebsite',methods=['GET'])
def extract_info_from_website():
    if request.method == 'GET':
        url = "https://edition.cnn.com/2018/08/21/asia/russia-largest-war-games-intl/index.html"
        words = ['the','celebs']
        recursion_depth = 2
        results= crawler.crawler_main(url,words,recursion_depth)
        return jsonify(results)
    else:
        return "Support only GET Method"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
