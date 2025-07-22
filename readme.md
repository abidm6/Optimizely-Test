# Getting & Setting up the project

### Running Test From Local Device
1. Clone the project at any location
2. Go to cloned project folder
3. Install all the dependencies by running the following command
      ```bash
       pip install -r requirements.txt
      ```

- **Running single testcase**

     ```bash
      pytest testsuiteFolder\subFolder1\...\subFolderN\test_module.py -k test_method_name
     ```

- **Running testsuite/module**

     ```bash
      pytest testsuiteRootFolder\subFolder01\...\subFolderN\test_module.py
     ```

- **Running testcases in a folder**

     ```bash
      pytest your_test_folder_name
     ```