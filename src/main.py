from multiprocessing.pool import ThreadPool
from model import get_model, predict
from time import sleep

def main():
    # TODO: remove everything and remake this main function
    pool = ThreadPool(processes=1)
    async_model = pool.apply_async(get_model)
    model = async_model.get(timeout=100)
    async_prediction = pool.apply_async(predict, (model, "cat_0.jpg"))
    prediction = async_prediction.get(timeout=10)
    print(f"Type expected: Cat; Acc: {prediction[1].cat * 100: .2f}%")

if __name__ == "__main__":
    main()
