import os
import re
import shutil
import subprocess

# Color codes for terminal output
class Colors:
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No color

# Directory structure constants
SRC_MAIN = "src/main/java"
SRC_TEST = "src/test/java"
POM_FILE = "pom.xml"
MAIN_FILE_NAME = "Main.java"
TEST_FILE_NAME = "MainTest.java"

# Cleanup function
def cleanup():
    print(f"{Colors.BLUE}Cleaning up Maven project directories...{Colors.NC}")
    for directory in ["target", SRC_MAIN, SRC_TEST, ".mvn"]:
        shutil.rmtree(directory, ignore_errors=True)
    if os.path.exists(POM_FILE):
        os.remove(POM_FILE)

# Find all Java files excluding specified patterns
def find_java_files():
    java_files = []
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith(".java") and file != TEST_FILE_NAME and "target" not in root:
                java_files.append(os.path.join(root, file))
    return java_files

# Rename the public class in a Java file to "Main" and update all references
def rename_class_to_main(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    match = re.search(r'public class ([A-Za-z0-9_]+)', content)
    if not match:
        print(f"Could not find public class in {file_path}")
        return

    original_class_name = match.group(1)
    print(f"Renaming class {original_class_name} in {file_path}")

    updated_content = re.sub(rf'\b{original_class_name}\b', "Main", content)

    with open(file_path, 'w') as f:
        f.write(updated_content)

def create_pom_file():
    pom_content = """<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>java-testing</artifactId>
    <version>1.0-SNAPSHOT</version>
    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.13.0</version>
                <configuration>
                    <release>11</release>
                </configuration>
            </plugin>
        </plugins>
    </build>

    <dependencies>
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter</artifactId>
            <version>5.9.2</version>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>com.fasterxml.jackson.core</groupId>
            <artifactId>jackson-databind</artifactId>
            <version>2.15.2</version>
        </dependency>
        <dependency>
            <groupId>org.json</groupId>
            <artifactId>json</artifactId>
            <version>20230227</version>
        </dependency>
        <dependency>
            <groupId>org.nd4j</groupId>
            <artifactId>nd4j-native-platform</artifactId>
            <version>1.0.0-M2.1</version>
        </dependency>

    </dependencies>
</project>"""

    with open(POM_FILE, "w") as f:
        f.write(pom_content)

# Run Maven commands
def run_maven():
    subprocess.run(["mvn", "clean", "test"], check=True)

# Main testing function
def run_tests():
    os.makedirs(SRC_MAIN, exist_ok=True)
    os.makedirs(SRC_TEST, exist_ok=True)

    shutil.copy(TEST_FILE_NAME, os.path.join(SRC_TEST, TEST_FILE_NAME))

    for file in find_java_files():
        rename_class_to_main(file)

        print(f"{Colors.GREEN}Processing file: {file}{Colors.NC}")

        shutil.copy(file, os.path.join(SRC_MAIN, MAIN_FILE_NAME))

        create_pom_file()

        try:
            run_maven()
        except subprocess.CalledProcessError as e:
            print(f"{Colors.RED}Error running tests for file: {file}{Colors.NC}")

        cleanup()
        os.makedirs(SRC_MAIN, exist_ok=True)
        os.makedirs(SRC_TEST, exist_ok=True)
        shutil.copy(TEST_FILE_NAME, os.path.join(SRC_TEST, TEST_FILE_NAME))
        # print separate line for each file
        print("-------------------------------------------------")

# Entry point of the script
def main():
    print(f"{Colors.GREEN}Starting Java code testing with Maven...{Colors.NC}")

    for file in find_java_files():
        rename_class_to_main(file)

    run_tests()

    print(f"{Colors.GREEN}All tests completed.{Colors.NC}")
    cleanup()

if __name__ == "__main__":
    main()
    cleanup()
