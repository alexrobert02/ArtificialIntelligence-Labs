from SeedsDataset import SeedsDataset


def main():
    file_path = "seeds_dataset.txt"
    seeds_data = SeedsDataset(file_path)

    parameters = seeds_data.train()
    print(f"Parameters: {parameters}")

    accuracy = seeds_data.evaluate_accuracy(seeds_data.x_test, seeds_data.y_test)
    print(f"Accuracy on test set: {accuracy}")

    confusion_mat = seeds_data.confusion_matrix(seeds_data.x_test, seeds_data.y_test)
    print("Confusion Matrix:")
    print(confusion_mat)

    precision_values = seeds_data.precision(seeds_data.x_test, seeds_data.y_test)
    recall_values = seeds_data.recall(seeds_data.x_test, seeds_data.y_test)
    f1_values = seeds_data.f1_score(seeds_data.x_test, seeds_data.y_test)

    print("Precision per class:")
    print(precision_values)
    print("Recall per class:")
    print(recall_values)
    print("F1 Score per class:")
    print(f1_values)


if __name__ == '__main__':
    main()
