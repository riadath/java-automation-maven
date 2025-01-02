# Java Testing Automation with Python

## Overview
This repository contains a Python script (`script.py`) to automate the testing process for Java files using Maven. The automation ensures all Java files are tested individually by renaming their public class and references to `Main`, compiling, and running them with a single test file (`MainTest.java`). This setup is designed for projects where multiple Java files are tested independently against a single unit test file.

## Nomenclature
- **`MainTest.java`** refers to the file containing the unit tests for your Java files.
- **`Main.java`** refers to the main code file after its public class has been renamed to `Main`.

## Important Notes
1. **Single Test File:**  
   - Ensure `MainTest.java` is the **only** test file in the directory, and it **must** be named exactly `MainTest.java`.  
   - This file should contain all the necessary JUnit tests.

2. **Java File Requirements:**  
   - Your repository can contain any number of Java files located anywhere within the directory (including subdirectories).  
   - All Java files (except `MainTest.java`) are automatically processed and renamed to `Main`.

3. **Self-Contained Files:**  
   - Ideally, `Main.java` and `MainTest.java` should be self-contained. Avoid importing additional classes from other files if possible.  
   - If `MainTest.java` needs to reference a helper class from your main code, declare it as a `public static class` **inside** `Main.java`. You can then access it in `MainTest.java` via `Main.ClassName`.

## Requirements
1. **Python** (Version 3.6 or later)  
   - [Download Python](https://www.python.org/downloads/) if you have not already.
   - Ensure `python` or `python3` is accessible in your PATH.

2. **Maven**  
   - [Download Maven](https://maven.apache.org/download.cgi) and follow the installation instructions.
   - Make sure the `mvn` command is accessible in your PATH.

## Directory Structure
A typical structure before running the script might look like:

```
.
├── MainTest.java      # Your single unit test file (mandatory)
├── script.py          # The Python script to automate testing
├── File1.java         # Example Java file
├── File2.java         # Another example Java file
└── Subdirectory/
    ├── File3.java
    └── File4.java
```

## How It Works (You can skip this section unless you are interested in the details)
1. **Renaming Classes:**
   - The script finds all Java files in your directory (excluding `MainTest.java` and build-related directories).
   - It renames the public class in each file to `Main` and updates all references to the original class name.

2. **Testing Each File:**
   - The script temporarily creates a Maven project structure (`src/main/java/` and `src/test/java/`) and places:
     - The renamed Java file into `src/main/java/Main.java`
     - The test file (`MainTest.java`) into `src/test/java/MainTest.java`
   - It then runs Maven to build and test the file.

3. **Cleanup:**
   - After testing each file, the script removes the temporary Maven project directories and any generated build artifacts. This ensures a clean environment before moving on to the next file.

## Adding Dependencies
To add a new dependency, edit the `create_pom_file` function in `script.py` and include the dependency block in the `<dependencies>` section. For example, to add the ND4J library:

```xml
<dependency>
    <groupId>org.nd4j</groupId>
    <artifactId>nd4j-native-platform</artifactId>
    <version>1.0.0-M2.1</version>
</dependency>
```

This ensures that the added library is included during the Maven build and test process.

## Usage
1. **Clone/Download** this repository or place `script.py` in your existing project directory.
2. Make sure your directory contains:
   - `MainTest.java` (with the correct name).
   - Any number of other Java files to be tested.
3. Open a terminal or command prompt in the project directory.
4. Run the script using the following command:

   ```bash
   python script.py
   ```

## Example Output
- The script will display messages indicating:
  - Which Java files are being renamed.
  - The result of each Maven test run (passed, failed, skipped).
  - Cleanup status after each file is processed.

## Final Cleanup
After all tests complete, the script automatically cleans the generated directories (`target`, `src`, `.mvn`, etc.). Your original Java files remain untouched (except for the in-place renaming to `Main`), and the workspace returns to a clean state.

---

