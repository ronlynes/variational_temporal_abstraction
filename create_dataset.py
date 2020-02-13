import numpy as np
import toml
from keras.datasets import mnist


def get_imgs():
    """
    mnistをロードして、0, 1, 3, 7, 9の画像を取り出す
    """
    (x_train, _), (_, _) = mnist.load_data()
    
    zero = x_train[1]
    one = x_train[3]
    three = x_train[7]
    seven = x_train[15]
    nine = x_train[4]

    files = [zero, one, three, seven, nine]
    return files


def preprocess(files):
    """
    paddingを行う (28x28 -> 32x32)
    """
    imgs = []

    for img in files:
        img = np.pad(img, [2, 2])
        imgs.append(img)
                    
    return imgs


def main():
    # parameters
    args = toml.load(open('config.toml'))['dataset']
    
    data_length = args['data_length']
    min_len = args['min_len']
    max_len = args['max_len']
    save_name = args['save_name']
    
    # start
    files = get_imgs()
    imgs = preprocess(files)
    
    # データセット作成
    file_num = len(files)
    cnt = 0
    data = np.empty((0, 32, 32))
    
    while cnt < data_length:
        #どの数字の画像を使うか
        idx = np.random.choice(file_num)
        
        # 同じ画像が連続する枚数
        num = np.random.choice(np.arange(min_len, max_len+1))
        
        # data_lengthを超える場合
        if cnt + num > data_length:
            num = data_length - cnt
        
        res = np.array([imgs[idx] for _ in range(num)])
        data = np.vstack((data, res))
        cnt = cnt + num
        
        # Log
        if cnt % 1000 == 0:
            print(cnt)
    
    #reshape (-1, 32, 32) -> (-1, 1, 32, 32)
    data = data.reshape(-1, 1, 32, 32)
    
    # 保存
    np.save(save_name, data)


if __name__ == '__main__':
    main()