# Large-Files-Processor
### Problem Statement :
Aim is to build a system which is able to handle long running processes in a distributed fashion. We need to be able to import products from a CSV file and into a database. There are half a million product details to be imported into the database. You can find the CSV file here in a compressed format Large File processing - Assignment.  After the import, we will run an aggregate query to give us no. of products with the same name.

### Introduction :
This repo provides a basic framework for aggregating CSV files with the same schema in a distributed fashion with a partial parallelism using threads and event loop. A data source is defined which hosts its data and staus. If there is a change in data at a given data source, the status changes. The Master Server continuously monitors this status via a HTTP call to the /sense endpoint hosted by each data source. Once, one pass of scanning is complete the fetching of data happens. The data once fetched is stored into a dataframe. Merging of data from all the data sources happens with a separate thread. After merging a groupby operation also takes place to club data on the basis of "name" and then everything is stored in the local sqlite database. User can

![1 - Setup](https://user-images.githubusercontent.com/53290539/113976502-dd2d1880-985e-11eb-9e29-0c76c1f06c52.JPG)
![2 - Setup](https://user-images.githubusercontent.com/53290539/113976518-e0c09f80-985e-11eb-9af8-46654a80b806.JPG)
![3 - Data Source 1](https://user-images.githubusercontent.com/53290539/113976525-e3bb9000-985e-11eb-9406-e8346f41a59b.JPG)
![4 - Data Source 2](https://user-images.githubusercontent.com/53290539/113976539-e74f1700-985e-11eb-968a-9a5c17847e7b.JPG)
![5 - Master Listener and Aggregator](https://user-images.githubusercontent.com/53290539/113976549-eae29e00-985e-11eb-8f1b-8b4708e388c7.JPG)
![6 - Reading DB](https://user-images.githubusercontent.com/53290539/113976565-ef0ebb80-985e-11eb-97f3-5e8620806c23.JPG)
![7 - Updation Form](https://user-images.githubusercontent.com/53290539/113976576-f209ac00-985e-11eb-87ea-a58fa915aa09.JPG)
![8 - Updation Form](https://user-images.githubusercontent.com/53290539/113976579-f5049c80-985e-11eb-9c6d-2bacc1eaab22.JPG)
![8 - Updation Form](https://user-images.githubusercontent.com/53290539/113976590-f7ff8d00-985e-11eb-9694-50528ec6aded.JPG)
