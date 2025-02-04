C:\mygit\BLazy\repo\codeorganize\code_organizer.py
Language detected: python
import os
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import shutil
from nltk.corpus import stopwords
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to walk through directories and collect Python files
def collect_python_files(directory):
    python_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files

# Function to parse Python file and extract features
def extract_features(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            tree = ast.parse(file.read())
            features = {
                'imports': [node.names[0].name for node in ast.walk(tree) if isinstance(node, ast.Import)],
                'functions': [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)],
                'classes': [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)],
                'docstrings': [ast.get_docstring(node) for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.ClassDef))],
                'comments': []  # Here you'd extract comments if needed
            }
            return features
        except Exception as e:
            logging.error(f'Failed to parse {file_path}: {e}')
            return None

# Function to process text features using TF-IDF vectorization
def process_features(features):
    text_data = [' '.join(filter(None, feature)) for feature in zip(features['imports'], features['functions'], features['docstrings'])]
    vectorizer = TfidfVectorizer(stop_words=stopwords.words('english'))
    tfidf_matrix = vectorizer.fit_transform(text_data)
    return tfidf_matrix, vectorizer

# Function to apply KMeans clustering
def apply_kmeans(tfidf_matrix, n_clusters=2):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(tfidf_matrix)
    return kmeans.labels_

# Function to generate cluster names
def generate_cluster_names(vectorizer, kmeans_labels):
    cluster_names = {}
    centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()
    for cluster_idx in range(len(set(kmeans_labels))):
        cluster_terms = [terms[ind] for ind in centroids[cluster_idx, :3]]
        cluster_names[cluster_idx] = ', '.join(cluster_terms)
    return cluster_names

# Function to create new directories and move files
def organize_files(python_files, kmeans_labels, cluster_names, output_dir):
    for file_path, label in zip(python_files, kmeans_labels):
        cluster_name = cluster_names[label]
        cluster_dir = os.path.join(output_dir, f'Cluster_{cluster_name}')
        if not os.path.exists(cluster_dir):
            os.makedirs(cluster_dir)
        shutil.copy2(file_path, cluster_dir)

# Main function
def main():
    source_dirs = [
        r'C:\mygit\BLazy\repo\codeorganize\llm_gen_code\directory_operations',
        r'C:\mygit\BLazy\repo\codeorganize\llm_gen_code\subprocess_operations'
    ]
    output_dir = r'C:\mygit\BLazy\repo\codeorganize\organized_code'

    all_python_files = []
    for dir_ in source_dirs:
        all_python_files.extend(collect_python_files(dir_))

    extracted_features = [extract_features(file) for file in all_python_files]

    tfidf_matrix, vectorizer = process_features(extracted_features)

    kmeans_labels = apply_kmeans(tfidf_matrix)

    cluster_names = generate_cluster_names(vectorizer, kmeans_labels)

    organize_files(all_python_files, kmeans_labels, cluster_names, output_dir)

if __name__ == '__main__':
    main()
C:\mygit\BLazy\repo\codeorganize\code_organizer.py
Language detected: python
# Your code goes here

# Required imports
import os
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.model_selection import GridSearchCV
import shutil
import nltk
from nltk.corpus import stopwords
import logging

# Download NLTK stopwords
nltk.download('stopwords')

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to walk through directories and collect Python files
def collect_python_files(directory):
    python_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files

# Function to parse Python file and extract features
def extract_features(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            tree = ast.parse(file.read())
            features = {
                'imports': [node.names[0].name for node in ast.walk(tree) if isinstance(node, ast.Import)],
                'functions': [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)],
                'classes': [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)],
                'docstrings': [ast.get_docstring(node) for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.ClassDef))],
                'comments': []  # Here you'd extract comments if needed
            }
            return features
        except Exception as e:
            logging.error(f'Failed to parse {file_path}: {e}')
            return None

# Function to process text features using TF-IDF vectorization
def process_features(features):
    text_data = [' '.join(map(str, filter(None, feature))) for feature in zip(
        [item for sublist in [feat.get('imports', []) for feat in features if feat] for item in sublist], 
        [item for sublist in [feat.get('functions', []) for feat in features if feat] for item in sublist],
        [item for sublist in [feat.get('docstrings', []) for feat in features if feat] for item in sublist])]
    
    vectorizer = TfidfVectorizer(stop_words=stopwords.words('english'))
    tfidf_matrix = vectorizer.fit_transform(text_data)
    return tfidf_matrix, vectorizer

# Function to determine optimal number of clusters using GridSearchCV
def determine_optimal_clusters(tfidf_matrix):
    params = {'n_clusters': list(range(2, 11))}
    grid = GridSearchCV(KMeans(), param_grid=params, cv=5)
    grid.fit(tfidf_matrix)
    return grid.best_params_['n_clusters']

# Function to apply KMeans clustering
def apply_kmeans(tfidf_matrix, n_clusters=None):
    if n_clusters is None:
        n_clusters = determine_optimal_clusters(tfidf_matrix)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(tfidf_matrix)
    return kmeans.labels_

# Function to generate cluster names
def generate_cluster_names(vectorizer, kmeans_labels):
    cluster_names = {}
    centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()
    for cluster_idx in range(len(set(kmeans_labels))):
        cluster_terms = [terms[ind] for ind in centroids[cluster_idx, :3]]
        cluster_names[cluster_idx] = ', '.join(cluster_terms)
    return cluster_names

# Function to create new directories and move files
def organize_files(python_files, kmeans_labels, cluster_names, output_dir):
    for file_path, label in zip(python_files, kmeans_labels):
        cluster_name = cluster_names[label]
        cluster_dir = os.path.join(output_dir, f'Cluster_{cluster_name}')
        if not os.path.exists(cluster_dir):
            os.makedirs(cluster_dir)
        shutil.copy2(file_path, cluster_dir)

# Main function
def main():
    source_dirs = [
        r'C:\mygit\BLazy\repo\codeorganize\llm_gen_code\directory_operations',
        r'C:\mygit\BLazy\repo\codeorganize\llm_gen_code\subprocess_operations'
    ]
    output_dir = r'C:\mygit\BLazy\repo\codeorganize\organized_code'

    all_python_files = []
    for dir_ in source_dirs:
        all_python_files.extend(collect_python_files(dir_))

    extracted_features = [extract_features(file) for file in all_python_files]

    # Filter out None values before processing
    filtered_extracted_features = [feat for feat in extracted_features if feat is not None]

    if not filtered_extracted_features:
        logging.error("No valid features extracted from provided files.")
        return

    tfidf_matrix, vectorizer = process_features(filtered_extracted_features)

    kmeans_labels = apply_kmeans(tfidf_matrix)

    cluster_names = generate_cluster_names(vectorizer, kmeans_labels)

    organize_files(all_python_files, kmeans_labels, cluster_names, output_dir)

if __name__ == '__main__':
    main()
C:\mygit\BLazy\repo\codeorganize\code_organizer.py
Language detected: python
# Your code goes here

# Required imports
import os
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import silhouette_score
import shutil
import nltk
from nltk.corpus import stopwords
import logging

# Download NLTK stopwords
nltk.download('stopwords')

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to walk through directories and collect Python files
def collect_python_files(directory):
    python_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files

# Function to parse Python file and extract features
def extract_features(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            tree = ast.parse(file.read())
            features = {
                'imports': [node.names[0].name for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))],
                'functions': [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)],
                'classes': [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)],
                'docstrings': [ast.get_docstring(node) for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.ClassDef))],
                'comments': []  # Here you'd extract comments if needed
            }
            return features
        except Exception as e:
            logging.error(f'Failed to parse {file_path}: {e}')
            return None

# Function to process text features using TF-IDF vectorization
def process_features(features):
    text_data = [' '.join(map(str, filter(None, feature))) for feature in zip(
        [item for sublist in [feat.get('imports', []) for feat in features if feat] for item in sublist],
        [item for sublist in [feat.get('functions', []) for feat in features if feat] for item in sublist],
        [item for sublist in [feat.get('docstrings', []) for feat in features if feat] for item in sublist])]

    vectorizer = TfidfVectorizer(stop_words=stopwords.words('english'))
    tfidf_matrix = vectorizer.fit_transform(text_data)
    return tfidf_matrix, vectorizer

# Function to determine optimal number of clusters using GridSearchCV with silhouette scoring
def determine_optimal_clusters(tfidf_matrix):
    silhouette_scores = []
    range_n_clusters = list(range(2, 11))
    
    for n_clusters in range_n_clusters:
        if len(tfidf_matrix) > n_clusters:
            kmeans = KMeans(n_clusters=n_clusters, random_state=42).fit(tfidf_matrix)
            labels = kmeans.labels_
            score = silhouette_score(tfidf_matrix, labels)
            silhouette_scores.append((n_clusters, score))

    best_n_clusters = max(silhouette_scores, key=lambda x: x[1])[0] if silhouette_scores else 2
    logging.info(f"Best number of clusters based on silhouette score: {best_n_clusters}")
    return best_n_clusters

# Function to apply KMeans clustering
def apply_kmeans(tfidf_matrix, n_clusters=None):
    if n_clusters is None:
        n_clusters = determine_optimal_clusters(tfidf_matrix)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(tfidf_matrix)
    return kmeans.labels_

# Function to generate cluster names
def generate_cluster_names(vectorizer, kmeans_labels):
    cluster_names = {}
    centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()
    for cluster_idx in range(len(set(kmeans_labels))):
        cluster_terms = [terms[ind] for ind in centroids[cluster_idx, :3]]
        cluster_names[cluster_idx] = ', '.join(cluster_terms)
    return cluster_names

# Function to create new directories and move files
def organize_files(python_files, kmeans_labels, cluster_names, output_dir):
    for file_path, label in zip(python_files, kmeans_labels):
        cluster_name = cluster_names[label]
        cluster_dir = os.path.join(output_dir, f'Cluster_{cluster_name}')
        if not os.path.exists(cluster_dir):
            os.makedirs(cluster_dir)
        shutil.copy2(file_path, os.path.join(cluster_dir, os.path.basename(file_path)))

# Main function
def main():
    source_dirs = [
        r'C:\mygit\BLazy\repo\codeorganize\llm_gen_code\directory_operations',
        r'C:\mygit\BLazy\repo\codeorganize\llm_gen_code\subprocess_operations'
    ]
    output_dir = r'C:\mygit\BLazy\repo\codeorganize\organized_code'

    all_python_files = []
    for dir_ in source_dirs:
        all_python_files.extend(collect_python_files(dir_))

    extracted_features = [extract_features(file) for file in all_python_files]

    # Filter out None values before processing
    filtered_extracted_features = [feat for feat in extracted_features if feat is not None]

    if not filtered_extracted_features:
        logging.error("No valid features extracted from provided files.")
        return

    tfidf_matrix, vectorizer = process_features(filtered_extracted_features)

    kmeans_labels = apply_kmeans(tfidf_matrix)

    cluster_names = generate_cluster_names(vectorizer, kmeans_labels)

    organize_files(all_python_files, kmeans_labels, cluster_names, output_dir)

if __name__ == '__main__':
    main()
C:\mygit\BLazy\repo\codeorganize\code_organizer.py
Language detected: python
import os
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import silhouette_score
import shutil
import nltk
from nltk.corpus import stopwords
import logging

# Download NLTK stopwords
nltk.download('stopwords')

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to walk through directories and collect Python files
def collect_python_files(directory):
    python_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files

# Function to parse Python file and extract features
def extract_features(file_path, file_mapping):
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            tree = ast.parse(file.read())
            file_name = os.path.basename(file_path)
            features = {
                'file_path': file_path,
                'imports': [node.names[0].name for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))],
                'functions': [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)],
                'classes': [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)],
                'docstrings': [ast.get_docstring(node) for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.ClassDef))],
                'comments': []  # Here you'd extract comments if needed
            }
            file_mapping[file_name] = features
            return features
        except Exception as e:
            logging.error(f'Failed to parse {file_path}: {e}')
            return None

# Function to process text features using TF-IDF vectorization
def process_features(features, file_mapping):
    file_contents = []
    file_names = []

    for file_name, feat in file_mapping.items():
        file_contents.append(' '.join(map(str, filter(None, [
            ' '.join(feat['imports']),
            ' '.join(feat['functions']),
            ' '.join(feat['docstrings'])
        ]))))
        file_names.append(file_name)

    vectorizer = TfidfVectorizer(stop_words=stopwords.words('english'))
    tfidf_matrix = vectorizer.fit_transform(file_contents)
    return tfidf_matrix, vectorizer, file_names

# Function to determine optimal number of clusters using GridSearchCV with silhouette scoring
def determine_optimal_clusters(tfidf_matrix):
    silhouette_scores = []
    range_n_clusters = list(range(2, 11))
    
    for n_clusters in range_n_clusters:
        if len(tfidf_matrix) > n_clusters:
            kmeans = KMeans(n_clusters=n_clusters, random_state=42).fit(tfidf_matrix)
            labels = kmeans.labels_
            score = silhouette_score(tfidf_matrix, labels)
            silhouette_scores.append((n_clusters, score))

    best_n_clusters = max(silhouette_scores, key=lambda x: x[1])[0] if silhouette_scores else 2
    logging.info(f"Best number of clusters based on silhouette score: {best_n_clusters}")
    return best_n_clusters

# Function to apply KMeans clustering
def apply_kmeans(tfidf_matrix, n_clusters=None):
    if n_clusters is None:
        n_clusters = determine_optimal_clusters(tfidf_matrix)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(tfidf_matrix)
    return kmeans.labels_

# Function to generate cluster names
def generate_cluster_names(vectorizer, kmeans_labels, file_names):
    cluster_names = {}
    centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()
    for cluster_idx in range(len(set(kmeans_labels))):
        cluster_terms = [terms[ind] for ind in centroids[cluster_idx, :3]]
        cluster_names[cluster_idx] = ', '.join(cluster_terms)
    return cluster_names

# Function to create new directories and move files
def organize_files(file_mapping, kmeans_labels, cluster_names, output_dir):
    for file_name, label in zip(file_mapping.keys(), kmeans_labels):
        file_path = file_mapping[file_name]['file_path']
        cluster_name = cluster_names[label]
        cluster_dir = os.path.join(output_dir, f'Cluster_{cluster_name}')
        if not os.path.exists(cluster_dir):
            os.makedirs(cluster_dir)
        shutil.copy2(file_path, os.path.join(cluster_dir, os.path.basename(file_path)))

# Main function
def main():
    source_dirs = [
        r'C:\mygit\BLazy\repo\codeorganize\llm_gen_code\directory_operations',
        r'C:\mygit\BLazy\repo\codeorganize\llm_gen_code\subprocess_operations'
    ]
    output_dir = r'C:\mygit\BLazy\repo\codeorganize\organized_code'

    file_mapping = {}

    all_python_files = []
    for dir_ in source_dirs:
        all_python_files.extend(collect_python_files(dir_))

    extracted_features = [extract_features(file, file_mapping) for file in all_python_files]

    # Filter out None values before processing
    filtered_extracted_features = {key: value for key, value in file_mapping.items() if value is not None}

    if not filtered_extracted_features:
        logging.error("No valid features extracted from provided files.")
        return

    tfidf_matrix, vectorizer, file_names = process_features(filtered_extracted_features, filtered_extracted_features)

    kmeans_labels = apply_kmeans(tfidf_matrix)

    cluster_names = generate_cluster_names(vectorizer, kmeans_labels, file_names)

    organize_files(filtered_extracted_features, kmeans_labels, cluster_names, output_dir)

if __name__ == '__main__':
    main()
C:\mygit\BLazy\repo\codeorganize\code_organizer.py
Language detected: python
# Your code goes here

import os
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import silhouette_score
import shutil
import nltk
from nltk.corpus import stopwords
import logging

# Download NLTK stopwords
nltk.download('stopwords')

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to walk through directories and collect Python files
def collect_python_files(directory):
    python_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files

# Function to parse Python file and extract features
def extract_features(file_path, file_mapping):
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            tree = ast.parse(file.read())
            file_name = os.path.basename(file_path)
            features = {
                'file_path': file_path,
                'imports': [node.names[0].name for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))],
                'functions': [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)],
                'classes': [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)],
                'docstrings': [ast.get_docstring(node) for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.ClassDef))],
                'comments': []  # Here you'd extract comments if needed
            }
            file_mapping[file_name] = features
            return features
        except Exception as e:
            logging.error(f'Failed to parse {file_path}: {e}')
            return None

# Function to process text features using TF-IDF vectorization
def process_features(features, file_mapping):
    file_contents = []
    file_names = []

    for file_name, feat in file_mapping.items():
        file_contents.append(' '.join(map(str, filter(None, [
            ' '.join(feat['imports']),
            ' '.join(feat['functions']),
            ' '.join(feat['docstrings'])
        ]))))
        file_names.append(file_name)

    vectorizer = TfidfVectorizer(stop_words=stopwords.words('english'))
    tfidf_matrix = vectorizer.fit_transform(file_contents)
    return tfidf_matrix, vectorizer, file_names

# Function to determine optimal number of clusters using GridSearchCV with silhouette scoring
def determine_optimal_clusters(tfidf_matrix):
    silhouette_scores = []
    range_n_clusters = list(range(2, 11))
    
    for n_clusters in range_n_clusters:
        if len(tfidf_matrix) > n_clusters:
            kmeans = KMeans(n_clusters=n_clusters, random_state=42).fit(tfidf_matrix)
            labels = kmeans.labels_
            score = silhouette_score(tfidf_matrix, labels)
            silhouette_scores.append((n_clusters, score))

    best_n_clusters = max(silhouette_scores, key=lambda x: x[1])[0] if silhouette_scores else 2
    logging.info(f"Best number of clusters based on silhouette score: {best_n_clusters}")
    return best_n_clusters

# Function to apply KMeans clustering
def apply_kmeans(tfidf_matrix, n_clusters=None):
    if n_clusters is None:
        n_clusters = determine_optimal_clusters(tfidf_matrix)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(tfidf_matrix)
    return kmeans.labels_

# Function to generate cluster names
def generate_cluster_names(vectorizer, kmeans_labels, file_names):
    cluster_names = {}
    centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()
    for cluster_idx in range(len(set(kmeans_labels))):
        cluster_terms = [terms[ind] for ind in centroids[cluster_idx, :3]]
        cluster_names[cluster_idx] = ', '.join(cluster_terms)
    return cluster_names

# Function to create new directories and move files
def organize_files(file_mapping, kmeans_labels, cluster_names, output_dir):
    for file_name, label in zip(file_mapping.keys(), kmeans_labels):
        file_path = file_mapping[file_name]['file_path']
        cluster_name = cluster_names[label]
        cluster_dir = os.path.join(output_dir, f'Cluster_{cluster_name}')
        if not os.path.exists(cluster_dir):
            os.makedirs(cluster_dir)
        shutil.copy2(file_path, os.path.join(cluster_dir, os.path.basename(file_path)))

# Main function
def main():
    source_dirs = [
        r'C:\mygit\BLazy\repo\codeorganize\new_reorganized_code'
    ]
    output_dir = r'C:\mygit\BLazy\repo\codeorganize\organized_code'

    file_mapping = {}

    all_python_files = []
    for dir_ in source_dirs:
        all_python_files.extend(collect_python_files(dir_))

    extracted_features = [extract_features(file, file_mapping) for file in all_python_files]

    # Filter out None values before processing
    filtered_extracted_features = {key: value for key, value in file_mapping.items() if value is not None}

    if not filtered_extracted_features:
        logging.error("No valid features extracted from provided files.")
        return

    tfidf_matrix, vectorizer, file_names = process_features(filtered_extracted_features, filtered_extracted_features)

    kmeans_labels = apply_kmeans(tfidf_matrix)

    cluster_names = generate_cluster_names(vectorizer, kmeans_labels, file_names)

    organize_files(filtered_extracted_features, kmeans_labels, cluster_names, output_dir)

if __name__ == '__main__':
    main()
C:\mygit\BLazy\repo\codeorganize\code_organizer.py
Language detected: python
# Your code goes here

import os
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import silhouette_score
import shutil
import nltk
from nltk.corpus import stopwords
import logging
import re
from datetime import datetime

# Download NLTK stopwords
nltk.download('stopwords')

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to extract version number from filename
def extract_version(filename):
    """Extract version number from filename."""
    match = re.search(r'v(\d+)', filename)
    return int(match.group(1)) if match else 0

# Improved function to walk through directories and collect Python files
def collect_python_files(directory):
    python_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                full_path = os.path.join(root, file)
                python_files.append((full_path, extract_version(file)))
    return sorted(python_files, key=lambda x: x[1])

# Improved function to parse Python file and extract features
def extract_features(file_path_info, file_mapping):
    file_path, _ = file_path_info
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            tree = ast.parse(file.read())
            file_name = os.path.basename(file_path)
            features = {
                'file_path': file_path,
                'imports': [node.names[0].name for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))],
                'functions': [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)],
                'classes': [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)],
                'docstrings': [ast.get_docstring(node) for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.ClassDef))],
                'comments': []  # Here you'd extract comments if needed
            }
            file_mapping[file_name] = features
            return features
    except Exception as e:
        logging.error(f'Failed to parse {file_path}: {e}')
        return None

# Improved function to process text features using TF-IDF vectorization
def process_features(features, file_mapping):
    file_contents = []
    file_names = []

    for file_name, feat in file_mapping.items():
        file_contents.append(' '.join(map(str, filter(None, [
            ' '.join(feat['imports']),
            ' '.join(feat['functions']),
            ' '.join(feat['docstrings'])
        ]))))
        file_names.append(file_name)

    vectorizer = TfidfVectorizer(stop_words=stopwords.words('english'))
    tfidf_matrix = vectorizer.fit_transform(file_contents)
    return tfidf_matrix, vectorizer, file_names

# Enhanced function to determine optimal number of clusters using GridSearchCV with silhouette scoring
def determine_optimal_clusters(tfidf_matrix):
    silhouette_scores = []
    range_n_clusters = list(range(2, 11))
    
    for n_clusters in range_n_clusters:
        if len(tfidf_matrix) > n_clusters:
            kmeans = KMeans(n_clusters=n_clusters, random_state=42).fit(tfidf_matrix)
            labels = kmeans.labels_
            score = silhouette_score(tfidf_matrix, labels)
            silhouette_scores.append((n_clusters, score))

    best_n_clusters = max(silhouette_scores, key=lambda x: x[1])[0] if silhouette_scores else 2
    logging.info(f"Best number of clusters based on silhouette score: {best_n_clusters}")
    return best_n_clusters

# Enhanced function to apply KMeans clustering
def apply_kmeans(tfidf_matrix, n_clusters=None):
    if n_clusters is None:
        n_clusters = determine_optimal_clusters(tfidf_matrix)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(tfidf_matrix)
    return kmeans.labels_

# Improved function to generate more descriptive cluster names
def generate_cluster_names(vectorizer, kmeans_labels, file_names):
    cluster_names = {}
    centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()
    for cluster_idx in range(len(set(kmeans_labels))):
        cluster_terms = [terms[ind] for ind in centroids[cluster_idx, :3]]
        cluster_names[cluster_idx] = ', '.join(cluster_terms)
    return cluster_names

# Improved function to create new directories and move files
def organize_files(file_mapping, kmeans_labels, cluster_names, output_dir):
    for file_name, label in zip(file_mapping.keys(), kmeans_labels):
        file_path = file_mapping[file_name]['file_path']
        cluster_name = cluster_names[label]
        cluster_dir = os.path.join(output_dir, f'Cluster_{cluster_name}')
        if not os.path.exists(cluster_dir):
            os.makedirs(cluster_dir)
        shutil.copy2(file_path, os.path.join(cluster_dir, os.path.basename(file_path)))

# Function to generate a detailed report
def generate_report(cluster_names, file_mapping):
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    report_file = os.path.join(output_dir, f"report_{now}.txt")
    with open(report_file, 'w') as report:
        for file_name, features in file_mapping.items():
            file_path = features['file_path']
            cluster_id = [k for k, v in cluster_names.items() if any(term in v for term in features['imports'])][0]
            report.write(f"{file_path} -> Cluster {cluster_id}\n")

# Main function
def main():
    source_dirs = [
        r'C:\mygit\BLazy\repo\codeorganize\new_reorganized_code'
    ]
    output_dir = r'C:\mygit\BLazy\repo\codeorganize\organized_code'

    file_mapping = {}

    all_python_files_info = []
    for dir_ in source_dirs:
        all_python_files_info.extend(collect_python_files(dir_))

    extracted_features = [extract_features(file_info, file_mapping) for file_info in all_python_files_info]

    # Filter out None values before processing
    filtered_extracted_features = {key: value for key, value in file_mapping.items() if value is not None}

    if not filtered_extracted_features:
        logging.error("No valid features extracted from provided files.")
        return

    tfidf_matrix, vectorizer, file_names = process_features(filtered_extracted_features, filtered_extracted_features)

    kmeans_labels = apply_kmeans(tfidf_matrix)

    cluster_names = generate_cluster_names(vectorizer, kmeans_labels, file_names)

    organize_files(filtered_extracted_features, kmeans_labels, cluster_names, output_dir)

    generate_report(cluster_names, file_mapping)

if __name__ == '__main__':
    main()
C:\mygit\BLazy\repo\codeorganize\code_organizer.py
Language detected: python
# Your code goes here

import os
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import silhouette_score
import shutil
import nltk
from nltk.corpus import stopwords
import logging
import re
from datetime import datetime

# Download NLTK stopwords
nltk.download('stopwords')

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to extract version number from filename
def extract_version(filename):
    """Extract version number from filename."""
    match = re.search(r'v(\d+)', filename)
    return int(match.group(1)) if match else 0

# Improved function to walk through directories and collect Python files
def collect_python_files(directory):
    python_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                full_path = os.path.join(root, file)
                python_files.append((full_path, extract_version(file)))
    return sorted(python_files, key=lambda x: x[1])

# Improved function to parse Python file and extract features
def extract_features(file_path_info, file_mapping):
    file_path, _ = file_path_info
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            tree = ast.parse(file.read())
            file_name = os.path.basename(file_path)
            features = {
                'file_path': file_path,
                'imports': [node.names[0].name for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))],
                'functions': [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)],
                'classes': [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)],
                'docstrings': [ast.get_docstring(node) for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.ClassDef))],
                'comments': []  # Here you'd extract comments if needed
            }
            file_mapping[file_name] = features
            return features
    except Exception as e:
        logging.error(f'Failed to parse {file_path}: {e}')
        return None

# Improved function to process text features using TF-IDF vectorization
def process_features(features, file_mapping):
    file_contents = []
    file_names = []

    for file_name, feat in file_mapping.items():
        file_contents.append(' '.join(map(str, filter(None, [
            ' '.join(feat['imports']),
            ' '.join(feat['functions']),
            ' '.join(feat['docstrings'])
        ]))))
        file_names.append(file_name)

    vectorizer = TfidfVectorizer(stop_words=stopwords.words('english'))
    tfidf_matrix = vectorizer.fit_transform(file_contents)
    return tfidf_matrix, vectorizer, file_names

# Enhanced function to determine optimal number of clusters using GridSearchCV with silhouette scoring
def determine_optimal_clusters(tfidf_matrix):
    silhouette_scores = []
    range_n_clusters = list(range(2, 11))
    
    for n_clusters in range_n_clusters:
        if len(tfidf_matrix) > n_clusters:
            kmeans = KMeans(n_clusters=n_clusters, random_state=42).fit(tfidf_matrix)
            labels = kmeans.labels_
            score = silhouette_score(tfidf_matrix, labels)
            silhouette_scores.append((n_clusters, score))

    best_n_clusters = max(silhouette_scores, key=lambda x: x[1])[0] if silhouette_scores else 2
    logging.info(f"Best number of clusters based on silhouette score: {best_n_clusters}")
    return best_n_clusters

# Enhanced function to apply KMeans clustering
def apply_kmeans(tfidf_matrix, n_clusters=None):
    if n_clusters is None:
        n_clusters = determine_optimal_clusters(tfidf_matrix)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(tfidf_matrix)
    return kmeans.labels_

# Improved function to generate more descriptive cluster names
def generate_cluster_names(vectorizer, kmeans_labels, file_names):
    cluster_names = {}
    centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()
    for cluster_idx in range(len(set(kmeans_labels))):
        cluster_terms = [terms[ind] for ind in centroids[cluster_idx, :3]]
        cluster_names[cluster_idx] = ', '.join(cluster_terms)
    return cluster_names

# Improved function to create new directories and move files
def organize_files(file_mapping, kmeans_labels, cluster_names, output_dir):
    for file_name, label in zip(file_mapping.keys(), kmeans_labels):
        file_path = file_mapping[file_name]['file_path']
        cluster_name = cluster_names[label]
        cluster_dir = os.path.join(output_dir, f'Cluster_{cluster_name}')
        if not os.path.exists(cluster_dir):
            os.makedirs(cluster_dir)
        shutil.copy2(file_path, os.path.join(cluster_dir, os.path.basename(file_path)))

# Function to generate a detailed report
def generate_report(cluster_names, file_mapping, output_dir):
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    report_file = os.path.join(output_dir, f"report_{now}.txt")
    with open(report_file, 'w') as report:
        for file_name, features in file_mapping.items():
            file_path = features['file_path']
            cluster_id = [k for k, v in cluster_names.items() if any(term in v for term in features['imports'])][0]
            report.write(f"{file_path} -> Cluster {cluster_id}\n")

# Main function
def main():
    source_dirs = [
        r'C:\mygit\BLazy\repo\codeorganize\new_reorganized_code'
    ]
    output_dir = r'C:\mygit\BLazy\repo\codeorganize\organized_code'

    file_mapping = {}

    all_python_files_info = []
    for dir_ in source_dirs:
        all_python_files_info.extend(collect_python_files(dir_))

    extracted_features = [extract_features(file_info, file_mapping) for file_info in all_python_files_info]

    # Filter out None values before processing
    filtered_extracted_features = {key: value for key, value in file_mapping.items() if value is not None}

    if not filtered_extracted_features:
        logging.error("No valid features extracted from provided files.")
        return

    tfidf_matrix, vectorizer, file_names = process_features(filtered_extracted_features, filtered_extracted_features)

    kmeans_labels = apply_kmeans(tfidf_matrix)

    cluster_names = generate_cluster_names(vectorizer, kmeans_labels, file_names)

    organize_files(filtered_extracted_features, kmeans_labels, cluster_names, output_dir)

    generate_report(cluster_names, filtered_extracted_features, output_dir)

if __name__ == '__main__':
    main()
C:\mygit\BLazy\repo\codeorganize\code_organizer.py
Language detected: python
# Your code goes here
import os
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import silhouette_score
import shutil
import nltk
from nltk.corpus import stopwords
import logging
import re
import time
from tqdm import tqdm
from collections import Counter

# Download NLTK stopwords
nltk.download('stopwords')

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to extract version number from filename
def extract_version(filename):
    """Extract version number from filename."""
    match = re.search(r'v(\d+)', filename)
    return int(match.group(1)) if match else 0

# Improved function to walk through directories and collect Python files
def collect_python_files(directory):
    python_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                full_path = os.path.join(root, file)
                python_files.append((full_path, extract_version(file)))
    return sorted(python_files, key=lambda x: x[1])

# Improved function to parse Python file and extract features
def extract_features(file_path_info, file_mapping):
    file_path, _ = file_path_info
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            tree = ast.parse(file.read())
            file_name = os.path.basename(file_path)
            features = {
                'file_path': file_path,
                'imports': [node.names[0].name for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))],
                'functions': [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)],
                'classes': [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)],
                'docstrings': [ast.get_docstring(node) for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.ClassDef))],
                'comments': []  # Here you'd extract comments if needed
            }
            file_mapping[file_name] = features
            return features
    except Exception as e:
        logging.error(f'Failed to parse {file_path}: {e}')
        return None

# Improved function to process text features using TF-IDF vectorization
def process_features(features, file_mapping):
    file_contents = []
    file_names = []

    for file_name, feat in file_mapping.items():
        file_contents.append(' '.join(map(str, filter(None, [
            ' '.join(feat['imports']),
            ' '.join(feat['functions']),
            ' '.join(feat['docstrings'])
        ]))))
        file_names.append(file_name)

    vectorizer = TfidfVectorizer(stop_words=stopwords.words('english'))
    tfidf_matrix = vectorizer.fit_transform(file_contents)
    return tfidf_matrix, vectorizer, file_names

# Enhanced function to determine optimal number of clusters using GridSearchCV with silhouette scoring
def determine_optimal_clusters(tfidf_matrix):
    silhouette_scores = []
    range_n_clusters = list(range(2, 11))
    
    for n_clusters in tqdm(range_n_clusters, desc="Determining optimal number of clusters"):
        if len(tfidf_matrix) > n_clusters:
            kmeans = KMeans(n_clusters=n_clusters, random_state=42).fit(tfidf_matrix)
            labels = kmeans.labels_
            score = silhouette_score(tfidf_matrix, labels)
            silhouette_scores.append((n_clusters, score))

    best_n_clusters = max(silhouette_scores, key=lambda x: x[1])[0] if silhouette_scores else 2
    logging.info(f"Best number of clusters based on silhouette score: {best_n_clusters}")
    return best_n_clusters

# Enhanced function to apply KMeans clustering
def apply_kmeans(tfidf_matrix, n_clusters=None):
    if n_clusters is None:
        n_clusters = determine_optimal_clusters(tfidf_matrix)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(tfidf_matrix)
    return kmeans.labels_

# Improved function to generate more descriptive cluster names
def generate_cluster_names(vectorizer, kmeans_labels, file_names):
    cluster_names = {}
    centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()
    for cluster_idx in range(len(set(kmeans_labels))):
        cluster_terms = [terms[ind] for ind in centroids[cluster_idx, :3]]
        cluster_names[cluster_idx] = ', '.join(cluster_terms)
    return cluster_names

# Improved function to create new directories and move files
def organize_files(file_mapping, kmeans_labels, cluster_names, output_dir):
    total_files = len(file_mapping)
    progress = 0
    
    for file_name, label in tqdm(list(file_mapping.items()), desc="Organizing files", total=total_files * 2):
        file_path = file_mapping[file_name]['file_path']
        cluster_name = cluster_names[label]
        cluster_dir = os.path.join(output_dir, f'Cluster_{cluster_name}')
        
        if not os.path.exists(cluster_dir):
            os.makedirs(cluster_dir)
        shutil.copy2(file_path, os.path.join(cluster_dir, os.path.basename(file_path)))
        progress += 1
        logging.info(f"File {file_name} organized into {cluster_dir}; Progress: {progress}/{total_files}")

# Improved function to generate a detailed report
def generate_report(cluster_names, file_mapping, output_dir):
    now = time.strftime('%Y-%m-%d_%H-%M-%S')
    report_file = os.path.join(output_dir, f"report_{now}.txt")
    with open(report_file, 'w') as report:
        for file_name, features in file_mapping.items():
            file_path = features['file_path']
            cluster_id = [k for k, v in cluster_names.items() if any(term in v for term in features['imports'])][0]
            report.write(f"{file_path} -> Cluster {cluster_id}\n")

# Function to gather cluster statistics
def generate_cluster_statistics(kmeans_labels):
    unique_clusters = set(kmeans_labels)
    cluster_counts = Counter(kmeans_labels)
    stats = {f"Cluster_{k}": count for k, count in cluster_counts.items()}
    return stats

# Main function
def main():
    source_dirs = [
        r'C:\mygit\BLazy\repo\codeorganize\new_reorganized_code'
    ]
    output_dir = r'C:\mygit\BLazy\repo\codeorganize\organized_code'

    file_mapping = {}

    all_python_files_info = []
    for dir_ in source_dirs:
        all_python_files_info.extend(collect_python_files(dir_))

    extracted_features = [extract_features(file_info, file_mapping) for file_info in all_python_files_info]

    # Filter out None values before processing
    filtered_extracted_features = {key: value for key, value in file_mapping.items() if value is not None}

    if not filtered_extracted_features:
        logging.error("No valid features extracted from provided files.")
        return

    tfidf_matrix, vectorizer, file_names = process_features(filtered_extracted_features, filtered_extracted_features)

    kmeans_labels = apply_kmeans(tfidf_matrix)

    cluster_names = generate_cluster_names(vectorizer, kmeans_labels, file_names)

    organize_files(filtered_extracted_features, kmeans_labels, cluster_names, output_dir)

    cluster_stats = generate_cluster_statistics(kmeans_labels)
    for cluster_name, count in cluster_stats.items():
        logging.info(f"Cluster {cluster_name} contains {count} files.")

    generate_report(cluster_names, filtered_extracted_features, output_dir)

if __name__ == '__main__':
    main()
