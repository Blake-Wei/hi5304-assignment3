# Running R in GitHub Codespaces

This guide demonstrates **two common ways to run R in GitHub Codespaces**:

1. Running R **inside a Jupyter Notebook**
2. Running R **from the terminal (command line)**

Both approaches are widely used in **health informatics**, research analytics, and data science workflows.

---

## 1. Running R in a Jupyter Notebook

Jupyter Notebooks allow you to combine **code, output, and narrative text** in one place. This is ideal for teaching, reproducible research, and exploratory data analysis.

### 1.1 Create or Open an R Notebook

1. In Codespaces, click **New File**
2. Name the file something like:
   ```
   analysis.ipynb
   ```
3. When prompted to select a kernel, choose **R (4.2.2)**

> **Important:** Always confirm that the notebook kernel shows **R (4.2.2)** at the top of the notebook. If the kernel changes, previously loaded packages and data may need to be reloaded.

If an R kernel is not available, you may need to install it (see instructor notes).

---

### 1.2 Run R Code in Notebook Cells

Each cell can contain R code. For example:

```r
# Check working directory
getwd()
```

```r
# Create a vector and compute the mean
x <- c(1, 2, 3, 4, 5)
mean(x)
```

---

### 1.3 Load Data Using Relative Paths

If your notebook is located in:
```
hi5304-notebooks/learning/
```

And your data is stored in:
```
hi5304-notebooks/data/
```

Use a relative path:

```r
patients_df <- read.csv("../data/patients.csv", stringsAsFactors = FALSE)
head(patients_df)
summary(patients_df)
```

---

### 1.4 Why Use R in Jupyter?

- Combines analysis and explanation
- Excellent for teaching and labs
- Supports reproducible research
- Easy to visualize results inline

---

## 2. Running R from the Terminal

Running R from the terminal is useful for **automation**, **batch analysis**, and understanding how analytics pipelines work behind the scenes.

---

### 2.1 Open the Terminal in Codespaces

In Codespaces:
- Click **Terminal → New Terminal**

You should see a prompt similar to:
```
/workspaces/hi5304-notebooks
```

---

### 2.2 Check That R Is Installed

Run:

```bash
R --version
```

If R is installed, the version information will be displayed.

---

### 2.3 Start an Interactive R Session

From the terminal, type:

```bash
R
```

You will see the R prompt:

```
>
```

You are now running R directly from the terminal.

---

### 2.4 Run R Commands in the Terminal

```r
getwd()

patients_df <- read.csv("data/patients.csv")
head(patients_df)
```

The working directory is usually the **project root** when running R from the terminal.

---

### 2.5 Exit R

To quit R:

```r
q()
```

Type `n` when asked to save the workspace.

---

### 2.6 Run an R Script from the Terminal

If you have an R script (for example, `analysis.R`):

```bash
Rscript analysis.R
```

This is commonly used for:
- Automated analyses
- Reproducible reports
- Data pipelines

---

## 3. Jupyter vs Terminal: When to Use Each

| Use Case | Jupyter Notebook | Terminal |
|--------|-----------------|----------|
| Teaching & labs | ✅ | ⚠️ |
| Exploratory analysis | ✅ | ⚠️ |
| Automation & pipelines | ⚠️ | ✅ |
| Reproducible scripts | ⚠️ | ✅ |
| Narrative + code | ✅ | ❌ |

---

## 4. Key Takeaways

- Jupyter is best for **learning, explanation, and exploration**
- Terminal R is best for **automation and reproducibility**
- Health informatics workflows often use **both**

Understanding both approaches builds strong analytics literacy and prepares students for real-world informatics environments.

