**Note: This is an Unofficial Community Project**

# Writing your own courses

We have tried to simplify the process of writing new Interactive Courses as much as possible. In fact, one just needs to create a few YAML files and the course basically creates itself. Just follow the steps given below in proper order to create your own course.

## Creating the root directory

So first of all, each course needs its own directory. As you may notice the repo contains a `courses` directory, you will need to create a directory tree inside this folder to create a new course. Given below are some steps to help you with the process:

1. Create a new folder inside the courses directory. The name of this folder should ideally be the same as the name of the course. The folder's name is later going to be invoked in the command:
   `learn run courses\<folder_name>`
2. Move into the newly created folder, this is the root directory of the course.
3. Create a file called `course.yaml`. This file will contain all the necessary metadata related to the course.

### Writing the `course.yaml` file

The `course.yaml` contains a few mandatory fields that should be present. They are:

1. Course: Name of the course
2. Author: Name of the author
3. Chapters: A single string of chapters delimited by semi-colons (;)

Example of a `course.yaml` file:

```text
- Course: Introduction to Hub
  Description: Learn what Hub is all about, and why you should use it.
  Chapters: What is Hub?
  Author: Debaditya Pal
```

That's it, we like to keep it short and simple.

## Creating the chapters directory

Inside the root folder of the course, we must create a subfolder and name it `chapters`. This is where we are going to store all our chapters. This folder will contain multiple YAML files, each for one chapter as mentioned in the `course.yaml` file. The names of these YAML files must be a valid filename slug version of the name of the chapter as mentioned in `course.yaml`
For example:
**Chapter:** What is Hub?
**Filename:** what-is-hub.yaml

Each of these files will contain multiple Snippets through which the course content will be served on the terminal. The Snippets must be ordered in the way you want them to appear during the course.

## Creating Snippets

Inside every `chapter-name.yaml` file there are going to be multiple snippets. For now we support 3 types of snippets:

1. Text Snippets: Simply print something for the user to read. Expects no inputs.
2. MCQ Snippets: Provides a Question with Multiple Choice Answers. Expects the answer as an input from the user.
3. Code Snippet: Provides the user with a written prompt and then creates a Python sub-shell for the user to input some code. The code is then interpreted and checked for correctness.

### Text Snippets

Requires the following keys:

1. Category: Value should be `text` to identify the Snippet as a Text Snippet.
2. Prompt: A string that will be printed for the user to read when the snippet is executed.

Example:

```text
- Category: text
  Prompt: "Welcome to the TextSnippet Showcase!"
```

### MCQ Snippets

Requires the following keys:

1. Category: Value should be `mcq` to identify the Snippet as a MCQ Snippet.
2. Prompt: The Question that will be printed for the user to read when the snippet is executed.
3. Options: A list of options the user is expected to choose from
4. Answer: The correct answer. Must be an option.
5. Hints: Whenever the user selects an option, this accompanying text will be displayed to help them. You might keep multiple hints for each option individually, or a single hint for the entire question.

Example:

```text
- Category: mcq
  Prompt: "What do you think Hub is all about? Dont be afraid to get it wrong."
  Options:
  - A Dataset Streaming package for Optimized ML Pipelining
  - The central part of a wheel, from which the spokes radiate.
  - The effective centre of an activity, region, or network.
  - A network device that broadcasts data to every connected node.
  Answer: A Dataset Streaming package for Optimized ML Pipelining
  Hints:
  - "That's correct!"
  - "Wheels do have hubs, but we want to focus on Datasets."
  - "Activity Hot Zones are called hub, but we want to focus on Datasets."
  - "Computer Network Topologies do have hubs, but we want to focus on Datasets."
```

### Code Snippets

Requires the following keys:

1. Category: Value should be `code` to identify the Snippet as a Code Snippet.
2. Prompt: A string that will be printed for the user to read when the snippet is executed.
3. Answer: The code against which the user's code will be checked for correctness.
4. Hints: If the user's code is incorrect, this message will be displayed for help.

Example:

```text
- Category: code
  Prompt: |
  And the function should look like this...
  def show_label(ds, idx):
	  print(ds.labels[idx].numpy())
  Answer: |
  def show_label(ds, idx):
	  print(ds.labels[idx].numpy())
  Hints: "Check the names of the variables."
```

**Note:** For one line codes feel free to use strings. For multi-line codes like in the example use the literal scalar block style introduced with the `|` to maintain the indentation.
