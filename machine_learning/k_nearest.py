import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib.colors import ListedColormap
from sklearn import neighbors, datasets, metrics

#dir_name = ['Walk', 'Climb_stairs']
dir_name = ['nothing', 'open']
#index = 0
inputs = []
label = []
for class_name in dir_name:
	class_label = 0
	if class_name=='open':
		class_label = 1
	#dir_path = 'C:\\Users\\NakagawaMasafumi\\Documents\\HMP_Dataset\\'+class_name+'_stats\\'
	dir_path = 'C:\\Users\\NakagawaMasafumi\\Documents\\data\\'+class_name+'_stats\\'
	files = os.listdir(dir_path)

	for file in files:
		f = open(dir_path+file, 'r')
		i=0
		input = []
		for line in f:
			values = line.strip().split(',')
			for j in range(0, 4):
				input.append(float(values[j]))
				i += 1

		inputs.append(input)
		label.append(class_label)

inputs = np.array(inputs)
label = np.array(label)
indices = np.random.permutation(len(inputs))
inputs_train = inputs[indices[:-64]]
label_train = label[indices[:-64]]
inputs_test = inputs[indices[-64:]]
label_test = label[indices[-64:]]
#print(inputs)
#print(label)
#iris = datasets.load_iris() # 4次元、150サンプルのデータセットで
                            # 植物の萼（がく）の長さ、幅、 花びらの長さ、幅、単位はcm。
#iris_X = iris.data[:, :2]  # 4次元のうち、最初の2次元の特徴量だけを使用
#iris_y = iris.target # 正解ラベル, 0, 1, 2の3種類
#print(iris_X)
#print(iris_y)

#########################################
np.random.seed(0) # 乱数のシード設定、0じゃなくてもなんでもいい
#indices = np.random.permutation(len(iris_X)) # 0~149の数字をランダムに並び替え
# 140個のデータセットを105個の教師データと35個のテストデータに分ける
#iris_X_train = iris_X[indices[:-35]]
#iris_y_train = iris_y[indices[:-35]]
#iris_X_test = iris_X[indices[-35:]]
#iris_y_test = iris_y[indices[-35:]]

#########################################
cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF'])
cmap_bold = ListedColormap(['#FF0000', '#00FF00', '#0000FF'])

#########################################
h = 0.1 # メッシュサイズ
k_list = [1, 3, 5, 10] # k の数
weights_list =['uniform', 'distance']
score = np.zeros((len(k_list)*2,5)) # score

#########################################
#plt.figure(figsize=(8*len(k_list), 12))
threshold = 450
i = 1 # subplot用
for weights in weights_list:
	for k in k_list:
		clf = neighbors.KNeighborsClassifier(k, weights=weights)
		clf.fit(inputs_train, label_train)
		#x1_min, x1_max = iris_X[:, 0].min() - 1, iris_X[:, 0].max() + 1 # Xの1次元目の最小と最大を取得
		#x2_min, x2_max = iris_X[:, 1].min() - 1, iris_X[:, 1].max() + 1 # Xの2次元目の最小と最大を取得
		# x1_min から x1_max まで、x2_min から x2_max までの h 刻みの等間隔な格子状配列を生成
		#xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, h), np.arange(x2_min, x2_max, h))
		# メッシュ状の各点に対して予測 / .ravel()で一次元配列に変換し、np.c_[]でxx1, xx2をxx2ごとに合体
		#Z = clf.predict(np.c_[xx1.ravel(), xx2.ravel()])
		#Z = Z.reshape(xx1.shape) # 配列形式変更
		#plt.subplot(2,len(k_list),i) # 2行 × k_list列のグラフのi番目のグラフに
		#plt.pcolormesh(xx1, xx2, Z, cmap=cmap_light) # 学習結果をプロット
		#plt.scatter(iris_X_train[:, 0], iris_X_train[:, 1], c=iris_y_train, cmap=cmap_bold) # 教師データをプロット
		#plt.scatter(iris_X_test[:, 0], iris_X_test[:, 1], c=iris_y_test, cmap=cmap_light) # テストデータをプロット
		#plt.xlim(xx1.min(), xx1.max())
		#plt.ylim(xx2.min(), xx2.max())
		#plt.title("k = %i, weights = '%s'" % (k, weights), fontsize=30)
		#print(clf.predict_proba(inputs_test))
		distset = clf.kneighbors(inputs_test,k)[0]
		#print(distset)
		correct = 0
		incorrect = 0
		data_index = 0
		for dists in distset:
			data_index += 1
			for d in dists:
				if d > threshold:
					print('disorder at line:'+str(data_index))
					print(str(d))
					if label_test[data_index-1] > 1:
						#異常検知の正解数不正解数を記録
						correct += 1
					else:
						incorrect += 1

		print(str(correct)+'/'+str(incorrect))
		score[i-1,3] = k
		score[i-1,0] = metrics.f1_score(label_test, clf.predict(inputs_test),average='weighted')
		score[i-1,1] = metrics.precision_score(label_test, clf.predict(inputs_test))
		score[i-1,2] = metrics.recall_score(label_test,clf.predict(inputs_test))
		i = i + 1

#plt.show()

plt.figure(figsize=(10, 4))
i = 0
for weights in weights_list:
    plt.subplot(1,2,i+1)
    plt.plot(score[i*len(k_list):(i+1)*len(k_list),0])
    plt.plot(score[i*len(k_list):(i+1)*len(k_list),1])
    plt.plot(score[i*len(k_list):(i+1)*len(k_list),2])
    plt.xticks([0,1,2,3],k_list)
    plt.ylim(score[:,:3].min()-0.05, 1.05)
    plt.title("weights = %s" % weights)
    plt.legend(('f1', 'prec', 'recall'), loc='upper right')
    plt.xlabel("k_neighbors")
    plt.ylabel("f1, prec, recall")
    i = i + 1
plt.show()
