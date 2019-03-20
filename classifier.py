from sklearn.datasets import load_files
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn import metrics

language_data_folder = r'C:\Users\Imre\PycharmProjects\dirteszt\Webcrawl Excercise\crawl\data'
dataset = load_files(language_data_folder, encoding='utf-8', shuffle=True)

train_data, test_data, y_train, y_test = train_test_split(dataset.data, dataset.target, test_size=0.3)

vect = TfidfVectorizer(max_df=0.95, min_df=3)

my_clf = Pipeline([('vector', vect),
                   ('clf', LinearSVC(C=1000))])

my_clf.fit(train_data, y_train)

y_predicted = my_clf.predict(test_data)

# print(help(metrics.classification_report))
# print(metrics.classification_report(y_test, y_predicted, labels=range(13),
#                                     target_names=dataset.target_names))

test_sentences = ['Az iráni látogatáson lévő White tavalyi letartóztatásáról egy emigráns szervezet adott először hírt\
, ami egy kiszabadult fogolytól azt tudta meg, hogy 2018 októberében, egy Meshed városában lévő börtönben találkozott\
 vele.']

predicted = my_clf.predict(test_sentences)

for sent, pred in zip(test_sentences, predicted):
    print(f'SZÖVEG: {sent}\nTIPP: {dataset.target_names[pred]} ')