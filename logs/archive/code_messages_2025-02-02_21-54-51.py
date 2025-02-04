C:\mygit\BLazy\repo\codeorganize\code_classifier.py
Language detected: python
# Required imports
import os
import ast
import astroid
import shutil
import logging
from collections import Counter
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
import numpy as np

# Configure logging
logging.basicConfig(filename='script_log.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Define directories
base_dir = 'path_to_directory'
directories = ['directory_operations', 'subprocess_operations']

def parse_python_file(file_path):
    """
    Parse a python file to extract features like imported modules, function/class names, keywords, etc.
    """
    with open(file_path, 'r') as file:
        content = file.read()
    
    try:
        module_ast = astroid.parse(content)
    except Exception as e:
        logging.error(f"Failed to parse {file_path}: {e}")
        return None
    
    module_imports = [node.name for node in module_ast.body if isinstance(node, astroid.Import)]
    class_names = [klass.name for klass in module_ast.classes]
    func_names = [func.name for func in module_ast.functions]
    keywords_used = [node.keyword for node in module_ast.nodes_of_class(astroid.Keyword)]

    common_operations = {
        'file_ops': ['open', 'read', 'write'],
        'subprocess_calls': ['call', 'run']
    }
    op_counts = Counter()
    
    for node in module_ast.nodes_of_class((astroid.Call, astroid.Assign)):
        if hasattr(node.func, 'name'):
            if any(op in node.func.name for op in common_operations['file_ops']):
                op_counts['file_ops'] += 1
            elif any(op in node.func.name for op in common_operations['subprocess_calls']):
                op_counts['subprocess_calls'] += 1
            
    return {
        'imports': module_imports,
        'class_names': class_names,
        'function_names': func_names,
        'keywords': keywords_used,
        'common_operations': dict(op_counts),
        'content': content
    }

def extract_features(directory_path):
    """
    Extract features from all .py files in the given directory.
    """
    features_list = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                features = parse_python_file(file_path)
                if features:
                    features_list.append(features)
    
    return features_list

def generate_feature_vectors(features_list):
    """
    Convert extracted features into a format suitable for clustering.
    """
    vectorizer = TfidfVectorizer()
    combined_content = "\n".join(feature['content'] for feature in features_list)
    
    transformed = vectorizer.fit_transform([combined_content])
    feature_names = vectorizer.get_feature_names_out()
    
    feature_vectors = []
    for feature in features_list:
        current_tfidf = vectorizer.transform([feature['content']])
        vector = [current_tfidf.toarray()[0][i] if any(word in feature['content'] for word in feature_names) else 0 for i in range(len(feature_names))]
        feature_vector = [
            len(feature['imports']), len(feature['class_names']), len(feature['function_names']),
            sum(feature['common_operations'].get('file_ops', 0), feature['common_operations'].get('subprocess_calls', 0)),
        ]
        
        vector.extend(feature_vector)
        feature_vectors.append(np.array(vector))
    
    return np.array(feature_vectors)

def cluster_files(feature_vectors, num_clusters=3):
    """
    Perform clustering using KMeans.
    """
    scaler = StandardScaler()
    scaled_vectors = scaler.fit_transform(feature_vectors)
    
    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(scaled_vectors)
    return kmeans.labels_

def organize_files(labels, features_list):
    """
    Organize files into named clusters.
    """
    clusters = {}
    for label, feature in zip(labels, features_list):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(feature)
    
    return clusters

def create_cluster_directories(base_dir, clusters):
    """
    Create directories for each cluster.
    """
    for label in clusters:
        dir_name = f'cluster_{label}'
        dir_path = os.path.join(base_dir, dir_name)
        os.makedirs(dir_path, exist_ok=True)

def move_files_to_clusters(base_dir, clusters):
    """
    Move files to respective cluster directories.
    """
    for label, features_list in clusters.items():
        dir_name = f'cluster_{label}'
        dir_path = os.path.join(base_dir, dir_name)
        
        for feature in features_list:
            src_path = os.path.dirname(feature['content'])
            dst_path = os.path.dirname(os.path.join(dir_path, feature['content']))
            try:
                shutil.move(src_path, dst_path)
                logging.info(f"Moved file from {src_path} to {dst_path}.")
            except Exception as e:
                logging.error(f"Failed to move file from {src_path} to {dst_path}: {e}")

def main():
    """
    Main function to orchestrate the entire process.
    """
    features_list = []
    for directory in directories:
        path = os.path.join(base_dir, directory)
        features_list.extend(extract_features(path))
        shutil.copytree(path, os.path.join(base_dir, f'backup_{directory}'), dirs_exist_ok=True)
        logging.info(f"Backup created for {directory}.")
    
    if features_list:
        feature_vectors = generate_feature_vectors(features_list)
        labels = cluster_files(feature_vectors)
        clusters = organize_files(labels, features_list)
        create_cluster_directories(base_dir, clusters)
        move_files_to_clusters(base_dir, clusters)
        logging.info("All operations completed successfully.")
    else:
        logging.warning("No Python files found for processing.")

if __name__ == "__main__":
    main()
C:\mygit\BLazy\repo\codeorganize\code_classifier.py
Language detected: python
# Required imports
import os
import ast
import astroid
import shutil
import logging
from collections import Counter
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
import numpy as np

# Configure logging
logging.basicConfig(filename='script_log.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Define directories
base_dir = r'C:\mygit\BLazy\repo\codeorganize\llm_gen_code'
directories = ['directory_operations', 'subprocess_operations']

def parse_python_file(file_path):
    """
    Parse a python file to extract features like imported modules, function/class names, keywords, etc.
    """
    if not os.path.isfile(file_path) or not file_path.endswith('.py'):
        logging.error(f"Invalid file: {file_path}")
        return None
    
    with open(file_path, 'r') as file:
        content = file.read()
    
    try:
        module_ast = astroid.parse(content)
    except Exception as e:
        logging.error(f"Failed to parse {file_path}: {e}")
        return None
    
    module_imports = [node.name for node in module_ast.body if isinstance(node, astroid.Import)]
    class_names = [klass.name for klass in module_ast.classes]
    func_names = [func.name for func in module_ast.functions]
    keywords_used = [node.keyword for node in module_ast.nodes_of_class(astroid.Keyword)]

    common_operations = {
        'file_ops': ['open', 'read', 'write'],
        'subprocess_calls': ['call', 'run']
    }
    op_counts = Counter()
    
    for node in module_ast.nodes_of_class((astroid.Call, astroid.Assign)):
        if hasattr(node.func, 'name'):
            if any(op in node.func.name for op in common_operations['file_ops']):
                op_counts['file_ops'] += 1
            elif any(op in node.func.name for op in common_operations['subprocess_calls']):
                op_counts['subprocess_calls'] += 1
            
    return {
        'file_path': file_path,
        'imports': module_imports,
        'class_names': class_names,
        'function_names': func_names,
        'keywords': keywords_used,
        'common_operations': dict(op_counts),
        'content': content
    }

def extract_features(directory_path):
    """
    Extract features from all .py files in the given directory.
    """
    features_list = []
    if not os.path.isdir(directory_path):
        logging.error(f"Directory does not exist: {directory_path}")
        return features_list
    
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                features = parse_python_file(file_path)
                if features:
                    features_list.append(features)
    
    return features_list

def generate_feature_vectors(features_list):
    """
    Convert extracted features into a format suitable for clustering.
    """
    vectorizer = TfidfVectorizer()
    combined_content = "\n".join(feature['content'] for feature in features_list)
    
    transformed = vectorizer.fit_transform([combined_content])
    feature_names = vectorizer.get_feature_names_out()
    
    feature_vectors = []
    for feature in features_list:
        current_tfidf = vectorizer.transform([feature['content']])
        vector = [current_tfidf.toarray()[0][i] if any(word in feature['content'] for word in feature_names) else 0 for i in range(len(feature_names))]
        feature_vector = [
            len(feature['imports']), len(feature['class_names']), len(feature['function_names']),
            sum(feature['common_operations'].get('file_ops', 0), feature['common_operations'].get('subprocess_calls', 0)),
        ]
        
        vector.extend(feature_vector)
        feature_vectors.append(np.array(vector))
    
    return np.array(feature_vectors)

def cluster_files(feature_vectors, num_clusters=3):
    """
    Perform clustering using KMeans.
    """
    scaler = StandardScaler()
    scaled_vectors = scaler.fit_transform(feature_vectors)
    
    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(scaled_vectors)
    return kmeans.labels_

def organize_files(labels, features_list):
    """
    Organize files into named clusters.
    """
    clusters = {}
    for label, feature in zip(labels, features_list):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(feature)
    
    return clusters

def validate_input_directories(directories):
    """
    Validate input directories.
    """
    valid_directories = []
    for directory in directories:
        directory_path = os.path.join(base_dir, directory)
        if os.path.isdir(directory_path):
            valid_directories.append(directory_path)
        else:
            logging.error(f"Directory does not exist: {directory_path}")
    
    return valid_directories

def create_cluster_directories(base_dir, clusters):
    """
    Create directories for each cluster.
    """
    for label in clusters:
        dir_name = f'cluster_{label}'
        dir_path = os.path.join(base_dir, dir_name)
        os.makedirs(dir_path, exist_ok=True)

def move_files_to_clusters(base_dir, clusters):
    """
    Move files to respective cluster directories while preserving original file structure.
    """
    for label, features_list in clusters.items():
        dir_name = f'cluster_{label}'
        dir_path = os.path.join(base_dir, dir_name)
        
        for feature in features_list:
            src_dir = os.path.dirname(feature['file_path'])
            relative_path = os.path.relpath(src_dir, base_dir)
            dst_path = os.path.join(dir_path, relative_path)
            
            try:
                if not os.path.exists(dst_path):
                    os.makedirs(dst_path, exist_ok=True)
                shutil.move(feature['file_path'], dst_path)
                logging.info(f"Moved file from {src_dir} to {dst_path}.")
            except Exception as e:
                logging.error(f"Failed to move file from {src_dir} to {dst_path}: {e}")

def analyze_cluster_contents(clusters):
    """
    Analyze cluster contents and generate meaningful names based on file content.
    """
    cluster_names = {}
    for label, features_list in clusters.items():
        content_summary = " ".join(feature['content'][:100] for feature in features_list)
        name = f"cluster_{label}_{content_summary[:10]}"
        cluster_names[label] = name
    
    return cluster_names

def main():
    """
    Main function to orchestrate the entire process.
    """
    validated_directories = validate_input_directories(directories)
    features_list = []
    for directory in validated_directories:
        features_list.extend(extract_features(directory))
        backup_dir = os.path.join(base_dir, f'backup_{os.path.basename(directory)}')
        os.makedirs(backup_dir, exist_ok=True)
        shutil.copytree(directory, backup_dir, dirs_exist_ok=True)
        logging.info(f"Backup created for {directory}.")
    
    if features_list:
        feature_vectors = generate_feature_vectors(features_list)
        labels = cluster_files(feature_vectors)
        clusters = organize_files(labels, features_list)
        cluster_names = analyze_cluster_contents(clusters)
        
        create_cluster_directories(base_dir, clusters)
        move_files_to_clusters(base_dir, clusters)
        
        for label, name in cluster_names.items():
            os.rename(os.path.join(base_dir, f'cluster_{label}'), os.path.join(base_dir, name))
            logging.info(f"Renamed {label} to {name}.")
        
        logging.info("All operations completed successfully.")
    else:
        logging.warning("No Python files found for processing.")

if __name__ == "__main__":
    main()
C:\mygit\BLazy\repo\codeorganize\code_classifier_v2.py
Language detected: python
# Required imports
import os
import ast
import astroid
import shutil
import logging
from pathlib import Path
from collections import Counter
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
import numpy as np
import json

# Configure logging
logging.basicConfig(filename='script_log.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Define directories
base_dir = r'C:\mygit\BLazy\repo\codeorganize'
ignore_dirs = ['*.venv*', 'cq-gridfinity']
code_clusters_dir = os.path.join(base_dir, 'code_clusters')
os.makedirs(code_clusters_dir, exist_ok=True)

def parse_python_file(file_path):
    """
    Parse a python file to extract features like imported modules, function/class names, keywords, etc.
    """
    if not os.path.isfile(file_path) or not file_path.endswith('.py'):
        logging.error(f"Invalid file: {file_path}")
        return None
    
    with open(file_path, 'r') as file:
        content = file.read()
    
    try:
        module_ast = astroid.parse(content)
    except Exception as e:
        logging.error(f"Failed to parse {file_path}: {e}")
        return None
    
    module_imports = [node.name for node in module_ast.body if isinstance(node, astroid.Import)]
    class_names = [klass.name for klass in module_ast.classes]
    func_names = [func.name for func in module_ast.functions]
    keywords_used = [node.keyword for node in module_ast.nodes_of_class(astroid.Keyword)]

    common_operations = {
        'file_ops': ['open', 'read', 'write'],
        'subprocess_calls': ['call', 'run']
    }
    op_counts = Counter()
    
    for node in module_ast.nodes_of_class((astroid.Call, astroid.Assign)):
        if hasattr(node.func, 'name'):
            if any(op in node.func.name for op in common_operations['file_ops']):
                op_counts['file_ops'] += 1
            elif any(op in node.func.name for op in common_operations['subprocess_calls']):
                op_counts['subprocess_calls'] += 1
            
    return {
        'file_path': str(file_path),
        'imports': module_imports,
        'class_names': class_names,
        'function_names': func_names,
        'keywords': keywords_used,
        'common_operations': dict(op_counts),
        'content': content
    }

def extract_features(directory_path):
    """
    Extract features from all .py files in the given directory.
    """
    features_list = []
    if not os.path.isdir(directory_path):
        logging.error(f"Directory does not exist: {directory_path}")
        return features_list
    
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".py") and not any(ignore_dir in root for ignore_dir in ignore_dirs):
                file_path = os.path.join(root, file)
                features = parse_python_file(file_path)
                if features:
                    features_list.append(features)
    
    return features_list

def generate_feature_vectors(features_list):
    """
    Convert extracted features into a format suitable for clustering.
    """
    vectorizer = TfidfVectorizer()
    combined_content = "\n".join(feature['content'] for feature in features_list)
    
    transformed = vectorizer.fit_transform([combined_content])
    feature_names = vectorizer.get_feature_names_out()
    
    feature_vectors = []
    for feature in features_list:
        current_tfidf = vectorizer.transform([feature['content']])
        vector = [current_tfidf.toarray()[0][i] if any(word in feature['content'] for word in feature_names) else 0 for i in range(len(feature_names))]
        
        feature_vector = [
            len(feature['imports']), 
            len(feature['class_names']), 
            len(feature['function_names']),
            feature['common_operations']['file_ops'] + feature['common_operations']['subprocess_calls']
        ]
        
        vector.extend(feature_vector)
        feature_vectors.append(np.array(vector))
    
    return np.array(feature_vectors)

def cluster_files(feature_vectors, num_clusters=3):
    """
    Perform clustering using KMeans.
    """
    scaler = StandardScaler()
    scaled_vectors = scaler.fit_transform(feature_vectors)
    
    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(scaled_vectors)
    return kmeans.labels_

def organize_files(labels, features_list):
    """
    Organize files into named clusters.
    """
    clusters = {}
    for label, feature in zip(labels, features_list):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(feature)
    
    return clusters

def create_cluster_directories(code_clusters_dir, clusters):
    """
    Create directories for each cluster.
    """
    for label in clusters:
        dir_name = f'cluster_{label}'
        dir_path = os.path.join(code_clusters_dir, dir_name)
        os.makedirs(dir_path, exist_ok=True)

def move_files_to_clusters(base_dir, clusters):
    """
    Copy files to respective cluster directories while maintaining the original file structure.
    """
    for label, features_list in clusters.items():
        dir_name = f'cluster_{label}'
        dir_path = os.path.join(code_clusters_dir, dir_name)
        
        for feature in features_list:
            src_dir = os.path.dirname(feature['file_path'])
            relative_path = os.path.relpath(src_dir, base_dir)
            dst_path = os.path.join(dir_path, relative_path)
            
            try:
                if not os.path.exists(dst_path):
                    os.makedirs(dst_path, exist_ok=True)
                shutil.copy2(feature['file_path'], dst_path)  # Use copy2 to preserve metadata
                logging.info(f"Copied file from {src_dir} to {dst_path}.")
            except Exception as e:
                logging.error(f"Failed to copy file from {src_dir} to {dst_path}: {e}")

def analyze_cluster_contents(clusters):
    """
    Analyze cluster contents and generate meaningful names based on file content.
    """
    cluster_names = {}
    for label, features_list in clusters.items():
        content_summary = " ".join(feature['content'][:100] for feature in features_list)
        name = f"cluster_{label}_{content_summary[:10]}"
        cluster_names[label] = name
    
    return cluster_names

def rename_clusters(code_clusters_dir, cluster_names):
    """
    Rename cluster directories with generated cluster names.
    """
    for label, name in cluster_names.items():
        cluster_path = os.path.join(code_clusters_dir, f'cluster_{label}')
        new_cluster_path = os.path.join(code_clusters_dir, name)
        os.rename(cluster_path, new_cluster_path)
        logging.info(f"Renamed {cluster_path} to {new_cluster_path}.")

def main():
    """
    Main function to orchestrate the entire process.
    """
    features_list = []
    for root, dirs, files in os.walk(base_dir):
        for dir in dirs:
            full_dir_path = os.path.join(root, dir)
            if not any(ignore_dir in full_dir_path for ignore_dir in ignore_dirs):
                features_list.extend(extract_features(full_dir_path))
        break  # We only want to start at the base directory
    
    if features_list:
        feature_vectors = generate_feature_vectors(features_list)
        labels = cluster_files(feature_vectors)
        clusters = organize_files(labels, features_list)
        cluster_names = analyze_cluster_contents(clusters)
        
        create_cluster_directories(code_clusters_dir, clusters)
        move_files_to_clusters(base_dir, clusters)
        rename_clusters(code_clusters_dir, cluster_names)
        
        logging.info("All operations completed successfully.")
    else:
        logging.warning("No Python files found for processing.")

if __name__ == "__main__":
    main()
C:\mygit\BLazy\repo\codeorganize\code_classifier_v2.py
Language detected: python
import os
import ast
import astroid
import shutil
import logging
from pathlib import Path
from collections import Counter
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
import numpy as np
import json

# Configure logging
logging.basicConfig(filename='script_log.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Define directories
base_dir = r'C:\mygit\BLazy\repo\codeorganize'
ignore_dirs = ['*.venv*', 'cq-gridfinity']
code_clusters_dir = os.path.join(base_dir, 'code_clusters')
os.makedirs(code_clusters_dir, exist_ok=True)

def parse_python_file(file_path):
    """
    Parse a python file to extract features like imported modules, function/class names, keywords, etc.
    """
    if not os.path.isfile(file_path) or not file_path.endswith('.py'):
        logging.error(f"Invalid file: {file_path}")
        return None
    
    with open(file_path, 'r') as file:
        content = file.read()
    
    try:
        module_ast = astroid.parse(content)
    except Exception as e:
        logging.error(f"Failed to parse {file_path}: {e}")
        return None
    
    module_imports = [node.name for node in module_ast.body if isinstance(node, astroid.Import)]
    class_names = [klass.name for klass in module_ast.classes]
    func_names = [func.name for func in module_ast.functions]
    keywords_used = [node.keyword for node in module_ast.nodes_of_class(astroid.Keyword)]

    common_operations = {
        'file_ops': ['open', 'read', 'write'],
        'subprocess_calls': ['call', 'run']
    }
    op_counts = Counter()
    
    for node in module_ast.nodes_of_class((astroid.Call, astroid.Assign)):
        if hasattr(node.func, 'name'):
            if any(op in node.func.name for op in common_operations['file_ops']):
                op_counts['file_ops'] += 1
            elif any(op in node.func.name for op in common_operations['subprocess_calls']):
                op_counts['subprocess_calls'] += 1
            
    return {
        'file_path': str(file_path),
        'imports': module_imports,
        'class_names': class_names,
        'function_names': func_names,
        'keywords': keywords_used,
        'common_operations': dict(op_counts),
        'content': content
    }

def extract_features(directory_path):
    """
    Extract features from all .py files in the given directory.
    """
    features_list = []
    if not os.path.isdir(directory_path):
        logging.error(f"Directory does not exist: {directory_path}")
        return features_list
    
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".py") and not any(ignore_dir in root for ignore_dir in ignore_dirs):
                file_path = os.path.join(root, file)
                features = parse_python_file(file_path)
                if features:
                    features_list.append(features)
    
    return features_list

def generate_feature_vectors(features_list):
    """
    Convert extracted features into a format suitable for clustering.
    """
    vectorizer = TfidfVectorizer()
    combined_content = "\n".join(feature['content'] for feature in features_list)
    
    transformed = vectorizer.fit_transform([combined_content])
    feature_names = vectorizer.get_feature_names_out()
    
    feature_vectors = []
    for feature in features_list:
        current_tfidf = vectorizer.transform([feature['content']])
        vector = [current_tfidf.toarray()[0][i] if any(word in feature['content'] for word in feature_names) else 0 for i in range(len(feature_names))]
        
        feature_vector = [
            len(feature['imports']), 
            len(feature['class_names']), 
            len(feature['function_names']),
            feature['common_operations']['file_ops'] + feature['common_operations']['subprocess_calls']
        ]
        
        vector.extend(feature_vector)
        feature_vectors.append(np.array(vector))
    
    return np.array(feature_vectors)

def cluster_files(feature_vectors, num_clusters=6):
    """
    Perform clustering using KMeans.
    """
    scaler = StandardScaler()
    scaled_vectors = scaler.fit_transform(feature_vectors)
    
    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(scaled_vectors)
    return kmeans.labels_

def organize_files(labels, features_list):
    """
    Organize files into named clusters.
    """
    clusters = {}
    for label, feature in zip(labels, features_list):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(feature)
    
    return clusters

def create_cluster_directories(code_clusters_dir, clusters):
    """
    Create directories for each cluster.
    """
    for label in clusters:
        dir_name = f'cluster_{label}'
        dir_path = os.path.join(code_clusters_dir, dir_name)
        os.makedirs(dir_path, exist_ok=True)

def move_files_to_clusters(base_dir, clusters):
    """
    Copy files to respective cluster directories while maintaining the original file structure.
    """
    for label, features_list in clusters.items():
        dir_name = f'cluster_{label}'
        dir_path = os.path.join(code_clusters_dir, dir_name)
        
        for feature in features_list:
            src_dir = os.path.dirname(feature['file_path'])
            relative_path = os.path.relpath(src_dir, base_dir)
            dst_path = os.path.join(dir_path, relative_path)
            
            try:
                if not os.path.exists(dst_path):
                    os.makedirs(dst_path, exist_ok=True)
                shutil.copy2(feature['file_path'], dst_path)  # Use copy2 to preserve metadata
                logging.info(f"Copied file from {src_dir} to {dst_path}.")
            except Exception as e:
                logging.error(f"Failed to copy file from {src_dir} to {dst_path}: {e}")

def analyze_cluster_contents(clusters):
    """
    Analyze cluster contents and generate meaningful names based on file content.
    """
    cluster_names = {}
    for label, features_list in clusters.items():
        content_summary = " ".join(feature['content'][:100] for feature in features_list)
        name = f"cluster_{label}_{content_summary[:10]}"
        cluster_names[label] = name
    
    return cluster_names

def get_cluster_name_from_features(features_list):
    """
    Generate a descriptive name for clusters based on common features.
    """
    total_files = sum(map(lambda feature: 1 if any(x in feature['content'] for x in ['file', 'files', 'input', 'output']) else 0, features_list))
    total_classes = sum(map(lambda feature: 1 if any(x in feature['content'] for x in ['class', 'def', 'class ']) else 0, features_list))
    most_common_import = Counter([imp.split('.')[0] for imp in list(set([item for sublist in [feat['imports'] for feat in features_list] for item in sublist]) if imp.split('.')[0] != '__future__')]).most_common(1)[0][0]

    return f"{total_files}_files_{total_classes}_classes_{most_common_import}"

def generate_report(clusters):
    """
    Generate a report detailing the contents of each cluster.
    """
    report = {}
    for label, features_list in clusters.items():
        report[label] = {}
        report[label]['cluster_name'] = get_cluster_name_from_features(features_list)
        report[label]['file_summary'] = {
            'total_files': len(features_list),
            'files_with_io': sum(map(lambda feature: 1 if any(x in feature['content'] for x in ['file', 'files', 'input', 'output']) else 0, features_list)),
            'files_with_classes': sum(map(lambda feature: 1 if any(x in feature['content'] for x in ['class', 'def', 'class ']) else 0, features_list)),
            'top_import': Counter([imp.split('.')[0] for imp in list(set([item for sublist in [feat['imports'] for feat in features_list] for item in sublist]) if imp.split('.')[0] != '__future__')]).most_common(1)[0][0]
        }
    return report

def rename_clusters(code_clusters_dir, cluster_names):
    """
    Rename cluster directories with generated cluster names.
    """
    for label, name in cluster_names.items():
        cluster_path = os.path.join(code_clusters_dir, f'cluster_{label}')
        new_cluster_path = os.path.join(code_clusters_dir, name)
        os.rename(cluster_path, new_cluster_path)
        logging.info(f"Renamed {cluster_path} to {new_cluster_path}.")

def dump_report(base_dir, report):
    """
    Dump cluster report into a JSON file.
    """
    with open(os.path.join(base_dir, 'cluster_report.json'), 'w') as report_file:
        json.dump(report, report_file, indent=4)
    logging.info("Report dumped to JSON file.")

def main():
    """
    Main function to orchestrate the entire process.
    """
    features_list = []
    # Collect root-level files
    root_level_files = [file for file in Path(base_dir).rglob('*.py') if not any(ignore_dir in str(file) for ignore_dir in ignore_dirs)]
    features_list.extend([parse_python_file(str(file)) for file in root_level_files if parse_python_file(str(file))])

    # Collect from subdirectories
    for root, dirs, files in os.walk(base_dir):
        for dir in dirs:
            full_dir_path = os.path.join(root, dir)
            if not any(ignore_dir in full_dir_path for ignore_dir in ignore_dirs):
                features_list.extend(extract_features(full_dir_path))
    
    if features_list:
        feature_vectors = generate_feature_vectors(features_list)
        labels = cluster_files(feature_vectors)
        clusters = organize_files(labels, features_list)
        cluster_names = analyze_cluster_contents(clusters)
        
        create_cluster_directories(code_clusters_dir, clusters)
        move_files_to_clusters(base_dir, clusters)
        rename_clusters(code_clusters_dir, cluster_names)
        
        cluster_report = generate_report(clusters)
        dump_report(base_dir, cluster_report)
        
        logging.info("All operations completed successfully.")
    else:
        logging.warning("No Python files found for processing.")

if __name__ == "__main__":
    main()
C:\mygit\BLazy\repo\codeorganize\code_classifier_v2.py
Language detected: python
import os
import ast
import astroid
import shutil
import logging
from pathlib import Path
from collections import Counter
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
import numpy as np
import json

# Configure logging
logging.basicConfig(filename='script_log.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Define directories
base_dir = r'C:\mygit\BLazy\repo\codeorganize'
ignore_dirs = ['*.venv*', 'cq-gridfinity']
code_clusters_dir = os.path.join(base_dir, 'code_clusters')
os.makedirs(code_clusters_dir, exist_ok=True)

def parse_python_file(file_path):
    """
    Parse a python file to extract features like imported modules, function/class names, keywords, etc.
    """
    if not os.path.isfile(file_path) or not file_path.endswith('.py'):
        logging.error(f"Invalid file: {file_path}")
        return None
    
    with open(file_path, 'r') as file:
        content = file.read()
    
    try:
        module_ast = astroid.parse(content)
    except Exception as e:
        logging.error(f"Failed to parse {file_path}: {e}")
        return None
    
    module_imports = [node.name for node in module_ast.body if isinstance(node, astroid.Import)]
    class_names = [klass.name for klass in module_ast.classes]
    func_names = [func.name for func in module_ast.functions]
    keywords_used = [node.keyword for node in module_ast.nodes_of_class(astroid.Keyword)]

    common_operations = {
        'file_ops': ['open', 'read', 'write'],
        'subprocess_calls': ['call', 'run']
    }
    op_counts = Counter()
    
    for node in module_ast.nodes_of_class((astroid.Call, astroid.Assign)):
        if hasattr(node.func, 'name'):
            if any(op in node.func.name for op in common_operations['file_ops']):
                op_counts['file_ops'] += 1
            elif any(op in node.func.name for op in common_operations['subprocess_calls']):
                op_counts['subprocess_calls'] += 1
            
    return {
        'file_path': str(file_path),
        'imports': module_imports,
        'class_names': class_names,
        'function_names': func_names,
        'keywords': keywords_used,
        'common_operations': dict(op_counts),
        'content': content
    }

def extract_features(directory_path):
    """
    Extract features from all .py files in the given directory.
    """
    features_list = []
    if not os.path.isdir(directory_path):
        logging.error(f"Directory does not exist: {directory_path}")
        return features_list
    
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".py") and not any(ignore_dir in root for ignore_dir in ignore_dirs):
                file_path = os.path.join(root, file)
                features = parse_python_file(file_path)
                if features:
                    features_list.append(features)
    
    return features_list

def generate_feature_vectors(features_list):
    """
    Convert extracted features into a format suitable for clustering.
    """
    vectorizer = TfidfVectorizer()
    combined_content = "\n".join(feature['content'] for feature in features_list)
    
    transformed = vectorizer.fit_transform([combined_content])
    feature_names = vectorizer.get_feature_names_out()
    
    feature_vectors = []
    for feature in features_list:
        current_tfidf = vectorizer.transform([feature['content']])
        vector = [current_tfidf.toarray()[0][i] if any(word in feature['content'] for word in feature_names) else 0 for i in range(len(feature_names))]
        
        file_op_count = feature['common_operations'].get('file_ops', 0)
        subprocess_call_count = feature['common_operations'].get('subprocess_calls', 0)
        feature_vector = [
            len(feature['imports']), 
            len(feature['class_names']), 
            len(feature['function_names']),
            file_op_count + subprocess_call_count
        ]
        
        vector.extend(feature_vector)
        feature_vectors.append(np.array(vector))
    
    return np.array(feature_vectors)

def cluster_files(feature_vectors, num_clusters=6):
    """
    Perform clustering using KMeans.
    """
    scaler = StandardScaler()
    scaled_vectors = scaler.fit_transform(feature_vectors)
    
    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(scaled_vectors)
    return kmeans.labels_

def organize_files(labels, features_list):
    """
    Organize files into named clusters.
    """
    clusters = {}
    for label, feature in zip(labels, features_list):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(feature)
    
    return clusters

def create_cluster_directories(code_clusters_dir, clusters):
    """
    Create directories for each cluster.
    """
    for label in clusters:
        dir_name = f'cluster_{label}'
        dir_path = os.path.join(code_clusters_dir, dir_name)
        os.makedirs(dir_path, exist_ok=True)

def move_files_to_clusters(base_dir, clusters):
    """
    Copy files to respective cluster directories while maintaining the original file structure.
    """
    for label, features_list in clusters.items():
        dir_name = f'cluster_{label}'
        dir_path = os.path.join(code_clusters_dir, dir_name)
        
        for feature in features_list:
            src_dir = os.path.dirname(feature['file_path'])
            relative_path = os.path.relpath(src_dir, base_dir)
            dst_path = os.path.join(dir_path, relative_path)
            
            try:
                if not os.path.exists(dst_path):
                    os.makedirs(dst_path, exist_ok=True)
                shutil.copy2(feature['file_path'], dst_path)  # Use copy2 to preserve metadata
                logging.info(f"Copied file from {src_dir} to {dst_path}.")
            except Exception as e:
                logging.error(f"Failed to copy file from {src_dir} to {dst_path}: {e}")

def analyze_cluster_contents(clusters):
    """
    Analyze cluster contents and generate meaningful names based on file content.
    """
    def get_cluster_summary(features_list):
        content_summary_parts = []
        for feature in features_list:
            content_summary_parts.extend(feature['content'].split()[:50])
        return " ".join(content_summary_parts)

    cluster_names = {}
    for label, features_list in clusters.items():
        summary = get_cluster_summary(features_list)
        name = f"cluster_{label}_{summary[:50].replace(' ', '_')}"
        cluster_names[label] = name
    
    return cluster_names

def get_cluster_name_from_features(features_list):
    """
    Generate a descriptive name for clusters based on common features.
    """
    file_operation_count = sum(feature['common_operations']['file_ops'] for feature in features_list)
    class_counts = sum(feature['common_operations']['file_ops'] + feature['common_operations']['subprocess_calls'] for feature in features_list)
    top_import = Counter(feature['imports'] for feature in features_list).most_common(1)[0][0]

    return f"{file_operation_count}_files_{class_counts}_classes_{top_import}"

def generate_report(clusters):
    """
    Generate a report detailing the contents of each cluster.
    """
    report = {}
    for label, features_list in clusters.items():
        report[label] = {}
        report[label]['cluster_name'] = get_cluster_name_from_features(features_list)
        report[label]['file_summary'] = {
            'total_files': len(features_list),
            'files_with_io': sum(feature['common_operations']['file_ops'] for feature in features_list),
            'files_with_classes': sum(feature['common_operations']['file_ops'] + feature['common_operations']['subprocess_calls'] for feature in features_list),
            'top_import': Counter(feature['imports'] for feature in features_list).most_common(1)[0][0]
        }
    return report

def rename_clusters(code_clusters_dir, cluster_names):
    """
    Rename cluster directories with generated cluster names.
    """
    for label, name in cluster_names.items():
        cluster_path = os.path.join(code_clusters_dir, f'cluster_{label}')
        new_cluster_path = os.path.join(code_clusters_dir, name)
        os.rename(cluster_path, new_cluster_path)
        logging.info(f"Renamed {cluster_path} to {new_cluster_path}.")

def dump_report(base_dir, report):
    """
    Dump cluster report into a JSON file.
    """
    with open(os.path.join(base_dir, 'cluster_report.json'), 'w') as report_file:
        json.dump(report, report_file, indent=4)
    logging.info("Report dumped to JSON file.")

def main():
    """
    Main function to orchestrate the entire process.
    """
    features_list = []
    # Collect root-level files
    root_level_files = [file for file in Path(base_dir).rglob('*.py') if not any(ignore_dir in str(file) for ignore_dir in ignore_dirs)]
    features_list.extend([parse_python_file(str(file)) for file in root_level_files if parse_python_file(str(file))])

    # Collect from subdirectories
    for root, dirs, files in os.walk(base_dir):
        for dir in dirs:
            full_dir_path = os.path.join(root, dir)
            if not any(ignore_dir in full_dir_path for ignore_dir in ignore_dirs):
                features_list.extend(extract_features(full_dir_path))
    
    if features_list:
        feature_vectors = generate_feature_vectors(features_list)
        labels = cluster_files(feature_vectors)
        clusters = organize_files(labels, features_list)
        cluster_names = analyze_cluster_contents(clusters)
        
        create_cluster_directories(code_clusters_dir, clusters)
        move_files_to_clusters(base_dir, clusters)
        rename_clusters(code_clusters_dir, cluster_names)
        
        cluster_report = generate_report(clusters)
        dump_report(base_dir, cluster_report)
        
        logging.info("All operations completed successfully.")
    else:
        logging.warning("No Python files found for processing.")

if __name__ == "__main__":
    main()
C:\mygit\BLazy\repo\codeorganize\code_classifier_v2.py
Language detected: python
import os
import ast
import astroid
import shutil
import logging
from pathlib import Path
from collections import Counter
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
import numpy as np
import json

# Configure logging
logging.basicConfig(filename='script_log.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

# Define directories
base_dir = r'C:\mygit\BLazy\repo\codeorganize'
ignore_dirs = ['*.venv*', 'cq-gridfinity']
code_clusters_dir = os.path.join(base_dir, 'code_clusters')
os.makedirs(code_clusters_dir, exist_ok=True)

def parse_python_file(file_path):
    """
    Parse a python file to extract features like imported modules, function/class names, keywords, etc.
    """
    logging.debug(f"Parsing file: {file_path}")
    if not os.path.isfile(file_path) or not file_path.endswith('.py'):
        logging.error(f"Invalid file: {file_path}")
        return None
    
    with open(file_path, 'r') as file:
        content = file.read()
    
    try:
        module_ast = astroid.parse(content)
    except Exception as e:
        logging.error(f"Failed to parse {file_path}: {e}")
        return None
    
    module_imports = [node.name for node in module_ast.body if isinstance(node, astroid.Import)]
    class_names = [klass.name for klass in module_ast.classes]
    func_names = [func.name for func in module_ast.functions]
    keywords_used = [node.keyword for node in module_ast.nodes_of_class(astroid.Keyword)]

    common_operations = {
        'file_ops': ['open', 'read', 'write'],
        'subprocess_calls': ['call', 'run']
    }
    op_counts = Counter()
    
    for node in module_ast.nodes_of_class((astroid.Call, astroid.Assign)):
        if hasattr(node.func, 'name'):
            if any(op in node.func.name for op in common_operations['file_ops']):
                op_counts['file_ops'] += 1
            elif any(op in node.func.name for op in common_operations['subprocess_calls']):
                op_counts['subprocess_calls'] += 1
            
    return {
        'file_path': str(file_path),
        'imports': module_imports,
        'class_names': class_names,
        'function_names': func_names,
        'keywords': keywords_used,
        'common_operations': dict(op_counts),
        'content': content
    }

def extract_features(directory_path):
    """
    Extract features from all .py files in the given directory.
    """
    logging.debug(f"Extracting features from directory: {directory_path}")
    features_list = []
    if not os.path.isdir(directory_path):
        logging.error(f"Directory does not exist: {directory_path}")
        return features_list
    
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".py") and not any(ignore_dir in root for ignore_dir in ignore_dirs):
                file_path = os.path.join(root, file)
                features = parse_python_file(file_path)
                if features:
                    features_list.append(features)
                    

    return features_list

def generate_feature_vectors(features_list):
    """
    Convert extracted features into a format suitable for clustering.
    """
    logging.debug("Generating feature vectors")
    vectorizer = TfidfVectorizer()
    combined_content = "\n".join(feature['content'] for feature in features_list)
    
    transformed = vectorizer.fit_transform([combined_content])
    feature_names = vectorizer.get_feature_names_out()
    
    feature_vectors = []
    for feature in features_list:
        current_tfidf = vectorizer.transform([feature['content']])
        vector = [current_tfidf.toarray()[0][i] for i in range(len(feature_names)) if any(word in feature['content'] for word in feature_names)]
        
        file_op_count = feature['common_operations'].get('file_ops', 0)
        subprocess_call_count = feature['common_operations'].get('subprocess_calls', 0)
        feature_vector = [
            len(feature['imports']) if feature['imports'] else 0,
            len(feature['class_names']) if feature['class_names'] else 0,
            len(feature['function_names']) if feature['function_names'] else 0,
            file_op_count + subprocess_call_count
        ]
        
        vector.extend(feature_vector)
        feature_vectors.append(np.array(vector))
    
    return feature_vectors

def cluster_files(feature_vectors, num_clusters=6):
    """
    Perform clustering using KMeans.
    """
    logging.debug(f"Clustering files with {num_clusters} clusters")
    scaler = StandardScaler()
    scaled_vectors = scaler.fit_transform(feature_vectors)
    
    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(scaled_vectors)
    return kmeans.labels_

def organize_files(labels, features_list):
    """
    Organize files into named clusters.
    """
    clusters = {}
    for label, feature in zip(labels, features_list):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(feature)
    
    return clusters

def create_cluster_directories(code_clusters_dir, clusters):
    """
    Create directories for each cluster.
    """
    logging.debug("Creating cluster directories")
    for label in clusters:
        dir_name = f'cluster_{label}'
        dir_path = os.path.join(code_clusters_dir, dir_name)
        os.makedirs(dir_path, exist_ok=True)

def move_files_to_clusters(base_dir, clusters):
    """
    Copy files to respective cluster directories while maintaining the original file structure.
    """
    logging.debug("Moving files to clusters")
    for label, features_list in clusters.items():
        dir_name = f'cluster_{label}'
        dir_path = os.path.join(code_clusters_dir, dir_name)
        
        for feature in features_list:
            src_dir = os.path.dirname(feature['file_path'])
            relative_path = os.path.relpath(src_dir, base_dir)
            dst_path = os.path.join(dir_path, relative_path)
            
            try:
                if not os.path.exists(dst_path):
                    os.makedirs(dst_path, exist_ok=True)
                shutil.copy2(feature['file_path'], dst_path)  # Use copy2 to preserve metadata
                logging.info(f"Copied file from {src_dir} to {dst_path}.")
            except Exception as e:
                logging.error(f"Failed to copy file from {src_dir} to {dst_path}: {e}")

def analyze_cluster_contents(clusters):
    """
    Analyze cluster contents and generate meaningful names based on file content.
    """
    def get_cluster_summary(features_list):
        content_summary_parts = []
        for feature in features_list:
            content_summary_parts.extend(feature['content'].split()[:50])
        return " ".join(content_summary_parts)

    cluster_names = {}
    for label, features_list in clusters.items():
        summary = get_cluster_summary(features_list)
        name = f"cluster_{label}_{summary[:50].replace(' ', '_')}"
        cluster_names[label] = name
    
    return cluster_names

def get_cluster_name_from_features(features_list):
    """
    Generate a descriptive name for clusters based on common features.
    """
    logging.debug("Generating cluster names based on common features")
    file_operation_count = sum(feature['common_operations']['file_ops'] for feature in features_list)
    class_counts = sum(feature['common_operations']['file_ops'] + feature['common_operations']['subprocess_calls'] for feature in features_list)
    top_import = Counter(feature['imports']).most_common(1)[0][0] if features_list else 'None'

    return f"{file_operation_count}_files_{class_counts}_classes_{top_import}"

def generate_report(clusters):
    """
    Generate a report detailing the contents of each cluster.
    """
    report = {}
    for label, features_list in clusters.items():
        report[label] = {}
        report[label]['cluster_name'] = get_cluster_name_from_features(features_list)
        report[label]['file_summary'] = {
            'total_files': len(features_list),
            'files_with_io': sum(feature['common_operations']['file_ops'] for feature in features_list),
            'files_with_classes': sum(feature['common_operations']['file_ops'] + feature['common_operations']['subprocess_calls'] for feature in features_list),
            'top_import': Counter(feature['imports']).most_common(1)[0][0] if features_list else 'None'
        }
    return report

def rename_clusters(code_clusters_dir, cluster_names):
    """
    Rename cluster directories with generated cluster names.
    """
    logging.debug("Renaming clusters")
    for label, name in cluster_names.items():
        cluster_path = os.path.join(code_clusters_dir, f'cluster_{label}')
        new_cluster_path = os.path.join(code_clusters_dir, name)
        os.rename(cluster_path, new_cluster_path)
        logging.info(f"Renamed {cluster_path} to {new_cluster_path}.")

def dump_report(base_dir, report):
    """
    Dump cluster report into a JSON file.
    """
    logging.debug("Dumping report into JSON file")
    with open(os.path.join(base_dir, 'cluster_report.json'), 'w') as report_file:
        json.dump(report, report_file, indent=4)
    logging.info("Report dumped to JSON file.")

def main():
    """
    Main function to orchestrate the entire process.
    """
    logging.debug("Starting the main process")

    features_list = []
    # Collect root-level files
    root_level_files = [file for file in Path(base_dir).rglob('*.py') if not any(ignore_dir in str(file) for ignore_dir in ignore_dirs)]
    features_list.extend([parse_python_file(str(file)) for file in root_level_files if parse_python_file(str(file))])

    # Collect from subdirectories
    for root, dirs, files in os.walk(base_dir):
        for dir in dirs:
            full_dir_path = os.path.join(root, dir)
            if not any(ignore_dir in full_dir_path for ignore_dir in ignore_dirs):
                features_list.extend(extract_features(full_dir_path))

    if features_list:
        feature_vectors = generate_feature_vectors(features_list)
        labels = cluster_files(feature_vectors)
        clusters = organise_files(labels, features_list)
        cluster_names = analyse_cluster_contents(clusters)
        
        create_cluster_directories(code_clusters_dir, clusters)
        move_files_to_cluters(base_dir, clusters)
        rename_clusters(code_clusters_dir, cluster_names)
        
        cluster_report = generate_report(clusters)
        dump_report(base_dir, cluster_report)
        
        logging.info("All operations completed successfully.")
    else:
        logging.warning("No Python files found for processing.")

if __name__ == '__main__':
    main()
C:\mygit\BLazy\repo\codeorganize\code_classifier_v2.py
Language detected: python
import os
import ast
import astroid
import shutil
import logging
from pathlib import Path
from collections import Counter
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
import numpy as np
import json

# Configure logging
logging.basicConfig(filename='script_log.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

# Define directories
base_dir = r'C:\mygit\BLazy\repo\codeorganize'
ignore_dirs = ['*.venv*', 'cq-gridfinity']
code_clusters_dir = os.path.join(base_dir, 'code_clusters')
os.makedirs(code_clusters_dir, exist_ok=True)

def parse_python_file(file_path):
    """
    Parse a python file to extract features like imported modules, function/class names, keywords, etc.
    """
    logging.debug(f"Parsing file: {file_path}")
    if not os.path.isfile(file_path) or not file_path.endswith('.py'):
        logging.error(f"Invalid file: {file_path}")
        return None
    
    with open(file_path, 'r') as file:
        content = file.read()
    
    try:
        module_ast = astroid.parse(content)
    except Exception as e:
        logging.error(f"Failed to parse {file_path}: {e}")
        return None
    
    module_imports = [node.name for node in module_ast.body if isinstance(node, astroid.Import)]
    class_names = [klass.name for klass in module_ast.classes]
    func_names = [func.name for func in module_ast.functions]
    keywords_used = [node.keyword for node in module_ast.nodes_of_class(astroid.Keyword)]

    common_operations = {
        'file_ops': ['open', 'read', 'write'],
        'subprocess_calls': ['call', 'run']
    }
    op_counts = Counter()
    
    for node in module_ast.nodes_of_class((astroid.Call, astroid.Assign)):
        if hasattr(node.func, 'name'):
            if any(op in node.func.name for op in common_operations['file_ops']):
                op_counts['file_ops'] += 1
            elif any(op in node.func.name for op in common_operations['subprocess_calls']):
                op_counts['subprocess_calls'] += 1
            
    return {
        'file_path': str(file_path),
        'imports': module_imports,
        'class_names': class_names,
        'function_names': func_names,
        'keywords': keywords_used,
        'common_operations': dict(op_counts),
        'content': content
    }

def extract_features(directory_path):
    """
    Extract features from all .py files in the given directory.
    """
    logging.debug(f"Extracting features from directory: {directory_path}")
    features_list = []
    if not os.path.isdir(directory_path):
        logging.error(f"Directory does not exist: {directory_path}")
        return features_list
    
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".py") and not any(ignore_dir in root for ignore_dir in ignore_dirs):
                file_path = os.path.join(root, file)
                features = parse_python_file(file_path)
                if features:
                    features_list.append(features)
                    
    return features_list

def generate_feature_vectors(features_list):
    """
    Convert extracted features into a format suitable for clustering.
    """
    logging.debug("Generating feature vectors")
    vectorizer = TfidfVectorizer()
    combined_content = "\n".join(feature['content'] for feature in features_list)
    
    transformed = vectorizer.fit_transform([combined_content])
    feature_names = vectorizer.get_feature_names_out()
    
    feature_vectors = []
    for feature in features_list:
        current_tfidf = vectorizer.transform([feature['content']])
        vector = [current_tfidf.toarray()[0][i] for i in range(len(feature_names)) if any(word in feature['content'] for word in feature_names)]
        
        file_op_count = feature['common_operations'].get('file_ops', 0)
        subprocess_call_count = feature['common_operations'].get('subprocess_calls', 0)
        feature_vector = [
            len(feature['imports']) if feature['imports'] else 0,
            len(feature['class_names']) if feature['class_names'] else 0,
            len(feature['function_names']) if feature['function_names'] else 0,
            file_op_count + subprocess_call_count
        ]
        
        vector.extend(feature_vector)
        feature_vectors.append(np.array(vector))
    
    return feature_vectors

def cluster_files(feature_vectors, num_clusters=6):
    """
    Perform clustering using KMeans.
    """
    logging.debug(f"Clustering files with {num_clusters} clusters")
    scaler = StandardScaler()
    scaled_vectors = scaler.fit_transform(feature_vectors)
    
    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(scaled_vectors)
    return kmeans.labels_

def organize_files(labels, features_list):
    """
    Organize files into named clusters.
    """
    clusters = {}
    for label, feature in zip(labels, features_list):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(feature)
    
    return clusters

def create_cluster_directories(code_clusters_dir, clusters):
    """
    Create directories for each cluster.
    """
    logging.debug("Creating cluster directories")
    for label in clusters:
        dir_name = f'cluster_{label}'
        dir_path = os.path.join(code_clusters_dir, dir_name)
        os.makedirs(dir_path, exist_ok=True)

def move_files_to_clusters(base_dir, clusters):
    """
    Copy files to respective cluster directories while maintaining the original file structure.
    """
    logging.debug("Moving files to clusters")
    for label, features_list in clusters.items():
        dir_name = f'cluster_{label}'
        dir_path = os.path.join(code_clusters_dir, dir_name)
        
        for feature in features_list:
            src_dir = os.path.dirname(feature['file_path'])
            relative_path = os.path.relpath(src_dir, base_dir)
            dst_path = os.path.join(dir_path, relative_path)
            
            try:
                if not os.path.exists(dst_path):
                    os.makedirs(dst_path, exist_ok=True)
                shutil.copy2(feature['file_path'], dst_path)  # Use copy2 to preserve metadata
                logging.info(f"Copied file from {src_dir} to {dst_path}.")
            except Exception as e:
                logging.error(f"Failed to copy file from {src_dir} to {dst_path}: {e}")

def analyze_cluster_contents(clusters):
    """
    Analyze cluster contents and generate meaningful names based on file content.
    """
    def get_cluster_summary(features_list):
        content_summary_parts = []
        for feature in features_list:
            content_summary_parts.extend(feature['content'].split()[:50])
        return " ".join(content_summary_parts)

    cluster_names = {}
    for label, features_list in clusters.items():
        summary = get_cluster_summary(features_list)
        name = f"cluster_{label}_{summary[:50].replace(' ', '_')}"
        cluster_names[label] = name
    
    return cluster_names

def get_cluster_name_from_features(features_list):
    """
    Generate a descriptive name for clusters based on common features.
    """
    logging.debug("Generating cluster names based on common features")
    file_operation_count = sum(feature['common_operations']['file_ops'] for feature in features_list)
    class_counts = sum(feature['common_operations']['file_ops'] + feature['common_operations']['subprocess_calls'] for feature in features_list)
    top_import = Counter(feature['imports']).most_common(1)[0][0] if features_list else 'None'

    return f"{file_operation_count}_files_{class_counts}_classes_{top_import}"

def generate_report(clusters):
    """
    Generate a report detailing the contents of each cluster.
    """
    report = {}
    for label, features_list in clusters.items():
        report[label] = {}
        report[label]['cluster_name'] = get_cluster_name_from_features(features_list)
        report[label]['file_summary'] = {
            'total_files': len(features_list),
            'files_with_io': sum(feature['common_operations']['file_ops'] for feature in features_list),
            'files_with_classes': sum(feature['common_operations']['file_ops'] + feature['common_operations']['subprocess_calls'] for feature in features_list),
            'top_import': Counter(feature['imports']).most_common(1)[0][0] if features_list else 'None'
        }
    return report

def rename_clusters(code_clusters_dir, cluster_names):
    """
    Rename cluster directories with generated cluster names.
    """
    logging.debug("Renaming clusters")
    for label, name in cluster_names.items():
        cluster_path = os.path.join(code_clusters_dir, f'cluster_{label}')
        new_cluster_path = os.path.join(code_clusters_dir, name)
        os.rename(cluster_path, new_cluster_path)
        logging.info(f"Renamed {cluster_path} to {new_cluster_path}.")

def dump_report(base_dir, report):
    """
    Dump cluster report into a JSON file.
    """
    logging.debug("Dumping report into JSON file")
    with open(os.path.join(base_dir, 'cluster_report.json'), 'w') as report_file:
        json.dump(report, report_file, indent=4)
    logging.info("Report dumped to JSON file.")

def main():
    """
    Main function to orchestrate the entire process.
    """
    logging.debug("Starting the main process")

    try:
        features_list = []
        # Collect root-level files
        root_level_files = [file for file in Path(base_dir).rglob('*.py') if not any(ignore_dir in str(file) for ignore_dir in ignore_dirs)]
        features_list.extend([parse_python_file(str(file)) for file in root_level_files if parse_python_file(str(file))])

        # Collect from subdirectories
        for root, dirs, files in os.walk(base_dir):
            for dir in dirs:
                full_dir_path = os.path.join(root, dir)
                if not any(ignore_dir in full_dir_path for ignore_dir in ignore_dirs):
                    features_list.extend(extract_features(full_dir_path))
    
        if features_list:
            feature_vectors = generate_feature_vectors(features_list)
            labels = cluster_files(feature_vectors)
            clusters = organize_files(labels, features_list)
            cluster_names = analyze_cluster_contents(clusters)
            
            create_cluster_directories(code_clusters_dir, clusters)
            move_files_to_clusters(base_dir, clusters)
            rename_clusters(code_clusters_dir, cluster_names)
            
            cluster_report = generate_report(clusters)
            dump_report(base_dir, cluster_report)
            
            logging.info("All operations completed successfully.")
        else:
            logging.warning("No Python files found for processing.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    main()
C:\mygit\BLazy\repo\codeorganize\code_classifier_v2.py
Language detected: python
import os
import ast
import astroid
import shutil
import logging
from pathlib import Path
from collections import Counter
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
import numpy as np
import json

# Configure logging
logging.basicConfig(filename='script_log.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

# Define directories
base_dir = r'C:\mygit\BLazy\repo\codeorganize'
ignore_dirs = ['*.venv*', 'cq-gridfinity']
code_clusters_dir = os.path.join(base_dir, 'code_clusters')
os.makedirs(code_clusters_dir, exist_ok=True)

def parse_python_file(file_path):
    """
    Parse a python file to extract features like imported modules, function/class names, keywords, etc.
    """
    logging.debug(f"Parsing file: {file_path}")
    if not os.path.isfile(file_path) or not file_path.endswith('.py'):
        logging.error(f"Invalid file: {file_path}")
        return None
    
    with open(file_path, 'r') as file:
        content = file.read()
    
    try:
        module_ast = astroid.parse(content)
    except Exception as e:
        logging.error(f"Failed to parse {file_path}: {e}")
        return None
    
    module_imports = [node.name for node in module_ast.body if isinstance(node, (astroid.Import, astroid.ImportFrom))]
    class_names = [klass.name for klass in module_ast.classes]
    func_names = [func.name for func in module_ast.functions]
    keywords_used = [node.keyword for node in module_ast.nodes_of_class(astroid.Keyword)]

    common_operations = {
        'file_ops': ['open', 'read', 'write'],
        'subprocess_calls': ['call', 'run']
    }
    op_counts = Counter()
    
    for node in module_ast.nodes_of_class((astroid.Call, astroid.Assign)):
        if hasattr(node.func, 'name'):
            if any(op in node.func.name for op in common_operations['file_ops']):
                op_counts['file_ops'] += 1
            elif any(op in node.func.name for op in common_operations['subprocess_calls']):
                op_counts['subprocess_calls'] += 1
            
    return {
        'file_path': str(file_path),
        'imports': module_imports,
        'class_names': class_names,
        'function_names': func_names,
        'keywords': keywords_used,
        'common_operations': dict(op_counts),
        'content': content
    }

def extract_features(directory_path):
    """
    Extract features from all .py files in the given directory.
    """
    logging.debug(f"Extracting features from directory: {directory_path}")
    features_list = []
    if not os.path.isdir(directory_path):
        logging.error(f"Directory does not exist: {directory_path}")
        return features_list
    
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".py") and not any(ignore_dir in root for ignore_dir in ignore_dirs):
                file_path = os.path.join(root, file)
                features = parse_python_file(file_path)
                if features:
                    features_list.append(features)
                    
    return features_list

def generate_feature_vectors(features_list):
    """
    Convert extracted features into a format suitable for clustering.
    """
    logging.debug("Generating feature vectors")
    vectorizer = TfidfVectorizer()
    combined_content = "\n".join(feature['content'] for feature in features_list)
    
    transformed = vectorizer.fit_transform([combined_content])
    feature_names = vectorizer.get_feature_names_out()
    
    feature_vectors = []
    for feature in features_list:
        current_tfidf = vectorizer.transform([feature['content']])
        vector = [current_tfidf.toarray()[0][i] for i in range(len(feature_names)) if any(word in feature['content'] for word in feature_names)]
        
        file_op_count = feature['common_operations'].get('file_ops', 0)
        subprocess_call_count = feature['common_operations'].get('subprocess_calls', 0)
        feature_vector = [
            len(feature['imports']) if feature['imports'] else 0,
            len(feature['class_names']) if feature['class_names'] else 0,
            len(feature['function_names']) if feature['function_names'] else 0,
            file_op_count + subprocess_call_count
        ]
        
        vector.extend(feature_vector)
        feature_vectors.append(np.array(vector))
    
    return feature_vectors

def cluster_files(feature_vectors, num_clusters=6):
    """
    Perform clustering using KMeans.
    """
    logging.debug(f"Clustering files with {num_clusters} clusters")
    scaler = StandardScaler()
    scaled_vectors = scaler.fit_transform(feature_vectors)
    
    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(scaled_vectors)
    return kmeans.labels_

def organize_files(labels, features_list):
    """
    Organize files into named clusters.
    """
    clusters = {}
    for label, feature in zip(labels, features_list):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(feature)
    
    return clusters

def create_cluster_directories(code_clusters_dir, clusters):
    """
    Create directories for each cluster.
    """
    logging.debug("Creating cluster directories")
    for label in clusters:
        dir_name = f'cluster_{label}'
        dir_path = os.path.join(code_clusters_dir, dir_name)
        os.makedirs(dir_path, exist_ok=True)

def move_files_to_clusters(base_dir, clusters):
    """
    Copy files to respective cluster directories while maintaining the original file structure.
    """
    logging.debug("Moving files to clusters")
    for label, features_list in clusters.items():
        dir_name = f'cluster_{label}'
        dir_path = os.path.join(code_clusters_dir, dir_name)
        
        for feature in features_list:
            src_dir = os.path.dirname(feature['file_path'])
            relative_path = os.path.relpath(src_dir, base_dir)
            dst_path = os.path.join(dir_path, relative_path)
            
            try:
                if not os.path.exists(dst_path):
                    os.makedirs(dst_path, exist_ok=True)
                shutil.copy2(feature['file_path'], dst_path)  # Use copy2 to preserve metadata
                logging.info(f"Copied file from {src_dir} to {dst_path}.")
            except Exception as e:
                logging.error(f"Failed to copy file from {src_dir} to {dst_path}: {e}")

def analyze_cluster_contents(clusters):
    """
    Analyze cluster contents and generate meaningful names based on file content.
    """
    def get_cluster_summary(features_list):
        content_summary_parts = []
        for feature in features_list:
            content_summary_parts.extend(feature['content'].split()[:50])
        return " ".join(content_summary_parts)

    cluster_names = {}
    for label, features_list in clusters.items():
        summary = get_cluster_summary(features_list)
        name = f"cluster_{label}_{summary[:50].replace(' ', '_')}"
        cluster_names[label] = name
    
    return cluster_names

def get_cluster_name_from_features(features_list):
    """
    Generate a descriptive name for clusters based on common features.
    """
    logging.debug("Generating cluster names based on common features")
    file_operation_count = sum(feature['common_operations']['file_ops'] for feature in features_list)
    class_counts = sum(feature['common_operations']['file_ops'] + feature['common_operations']['subprocess_calls'] for feature in features_list)
    top_import = Counter(feature['imports']).most_common(1)[0][0] if features_list else 'None'

    return f"{file_operation_count}_files_{class_counts}_classes_{top_import}"

def generate_report(clusters):
    """
    Generate a report detailing the contents of each cluster.
    """
    report = {}
    for label, features_list in clusters.items():
        report[label] = {}
        report[label]['cluster_name'] = get_cluster_name_from_features(features_list)
        report[label]['file_summary'] = {
            'total_files': len(features_list),
            'files_with_io': sum(feature['common_operations']['file_ops'] for feature in features_list),
            'files_with_classes': sum(feature['common_operations']['file_ops'] + feature['common_operations']['subprocess_calls'] for feature in features_list),
            'top_import': Counter(feature['imports']).most_common(1)[0][0] if features_list else 'None'
        }
    return report

def rename_clusters(code_clusters_dir, cluster_names):
    """
    Rename cluster directories with generated cluster names.
    """
    logging.debug("Renaming clusters")
    for label, name in cluster_names.items():
        cluster_path = os.path.join(code_clusters_dir, f'cluster_{label}')
        new_cluster_path = os.path.join(code_clusters_dir, name)
        os.rename(cluster_path, new_cluster_path)
        logging.info(f"Renamed {cluster_path} to {new_cluster_path}.")

def dump_report(base_dir, report):
    """
    Dump cluster report into a JSON file.
    """
    logging.debug("Dumping report into JSON file")
    with open(os.path.join(base_dir, 'cluster_report.json'), 'w') as report_file:
        json.dump(report, report_file, indent=4)
    logging.info("Report dumped to JSON file.")

def main():
    """
    Main function to orchestrate the entire process.
    """
    logging.debug("Starting the main process")

    try:
        features_list = []
        # Collect root-level files
        root_level_files = [file for file in Path(base_dir).rglob('*.py') if not any(ignore_dir in str(file) for ignore_dir in ignore_dirs)]
        features_list.extend([parse_python_file(str(file)) for file in root_level_files if parse_python_file(str(file))])

        # Collect from subdirectories
        for root, dirs, files in os.walk(base_dir):
            for dir in dirs:
                full_dir_path = os.path.join(root, dir)
                if not any(ignore_dir in full_dir_path for ignore_dir in ignore_dirs):
                    features_list.extend(extract_features(full_dir_path))
    
        if features_list:
            feature_vectors = generate_feature_vectors(features_list)
            labels = cluster_files(feature_vectors)
            clusters = organize_files(labels, features_list)
            cluster_names = analyze_cluster_contents(clusters)
            
            create_cluster_directories(code_clusters_dir, clusters)
            move_files_to_clusters(base_dir, clusters)
            rename_clusters(code_clusters_dir, cluster_names)
            
            cluster_report = generate_report(clusters)
            dump_report(base_dir, cluster_report)
            
            logging.info("All operations completed successfully.")
        else:
            logging.warning("No Python files found for processing.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    main()
C:\mygit\BLazy\repo\codeorganize\code_classifier_v2.py
Language detected: python
import os
import ast
import astroid
import shutil
import logging
from pathlib import Path
from collections import Counter
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
import numpy as np
import json

# Configure logging
logging.basicConfig(filename='script_log.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

# Define directories
base_dir = r'C:\mygit\BLazy\repo\codeorganize'
ignore_dirs = ['*.venv*', 'cq-gridfinity']
code_clusters_dir = os.path.join(base_dir, 'code_clusters')
os.makedirs(code_clusters_dir, exist_ok=True)

def extract_import_names(node):
    """
    Helper function to extract import names from Import and ImportFrom nodes correctly.
    """
    if isinstance(node, astroid.Import):
        return [(name.name, None) for name in node.names]
    elif isinstance(node, astroid.ImportFrom):
        return [(node.modname, alias.as_string()) for alias in node.names]
    return []

def parse_python_file(file_path):
    """
    Parse a python file to extract features like imported modules, function/class names, keywords, etc.
    """
    logging.debug(f"Parsing file: {file_path}")
    if not os.path.isfile(file_path) or not file_path.endswith('.py'):
        logging.error(f"Invalid file: {file_path}")
        return None
    
    with open(file_path, 'r') as file:
        content = file.read()
    
    try:
        module_ast = astroid.parse(content)
    except Exception as e:
        logging.error(f"Failed to parse {file_path}: {e}")
        return None
    
    module_imports = []
    for node in module_ast.body:
        if isinstance(node, (astroid.Import, astroid.ImportFrom)):
            module_imports.extend(extract_import_names(node))
    
    module_import_names = list(set([alias for name, alias in module_imports]))
    
    class_names = [klass.name for klass in module_ast.classes]
    func_names = [func.name for func in module_ast.functions]
    keywords_used = [node.keyword for node in module_ast.nodes_of_class(astroid.Keyword)]

    common_operations = {
        'file_ops': ['open', 'read', 'write'],
        'subprocess_calls': ['call', 'run']
    }
    op_counts = Counter()
    
    for node in module_ast.nodes_of_class((astroid.Call, astroid.Assign)):
        if hasattr(node.func, 'name'):
            if any(op in node.func.name for op in common_operations['file_ops']):
                op_counts['file_ops'] += 1
            elif any(op in node.func.name for op in common_operations['subprocess_calls']):
                op_counts['subprocess_calls'] += 1
            
    return {
        'file_path': str(file_path),
        'imports': module_import_names,
        'class_names': class_names,
        'function_names': func_names,
        'keywords': keywords_used,
        'common_operations': dict(op_counts),
        'content': content
    }

def extract_features(directory_path):
    """
    Extract features from all .py files in the given directory.
    """
    logging.debug(f"Extracting features from directory: {directory_path}")
    features_list = []
    if not os.path.isdir(directory_path):
        logging.error(f"Directory does not exist: {directory_path}")
        return features_list
    
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".py") and not any(ignore_dir in root for ignore_dir in ignore_dirs):
                file_path = os.path.join(root, file)
                features = parse_python_file(file_path)
                if features:
                    features_list.append(features)
                    
    return features_list

def generate_feature_vectors(features_list):
    """
    Convert extracted features into a format suitable for clustering.
    """
    logging.debug("Generating feature vectors")
    vectorizer = TfidfVectorizer()
    combined_content = "\n".join(feature['content'] for feature in features_list)
    
    transformed = vectorizer.fit_transform([combined_content])
    feature_names = vectorizer.get_feature_names_out()
    
    feature_vectors = []
    for feature in features_list:
        current_tfidf = vectorizer.transform([feature['content']])
        vector = [current_tfidf.toarray()[0][i] for i in range(len(feature_names)) if any(word in feature['content'] for word in feature_names)]
        
        file_op_count = feature['common_operations'].get('file_ops', 0)
        subprocess_call_count = feature['common_operations'].get('subprocess_calls', 0)
        feature_vector = [
            len(feature['imports']) if feature['imports'] else 0,
            len(feature['class_names']) if feature['class_names'] else 0,
            len(feature['function_names']) if feature['function_names'] else 0,
            file_op_count + subprocess_call_count
        ]
        
        vector.extend(feature_vector)
        feature_vectors.append(np.array(vector))
    
    return feature_vectors

def cluster_files(feature_vectors, num_clusters=6):
    """
    Perform clustering using KMeans.
    """
    logging.debug(f"Clustering files with {num_clusters} clusters")
    scaler = StandardScaler()
    scaled_vectors = scaler.fit_transform(feature_vectors)
    
    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(scaled_vectors)
    return kmeans.labels_

def organize_files(labels, features_list):
    """
    Organize files into named clusters.
    """
    clusters = {}
    for label, feature in zip(labels, features_list):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(feature)
    
    return clusters

def create_cluster_directories(code_clusters_dir, clusters):
    """
    Create directories for each cluster.
    """
    logging.debug("Creating cluster directories")
    for label in clusters:
        dir_name = f'cluster_{label}'
        dir_path = os.path.join(code_clusters_dir, dir_name)
        os.makedirs(dir_path, exist_ok=True)

def move_files_to_clusters(base_dir, clusters):
    """
    Copy files to respective cluster directories while maintaining the original file structure.
    """
    logging.debug("Moving files to clusters")
    for label, features_list in clusters.items():
        dir_name = f'cluster_{label}'
        dir_path = os.path.join(code_clusters_dir, dir_name)
        
        for feature in features_list:
            src_dir = os.path.dirname(feature['file_path'])
            relative_path = os.path.relpath(src_dir, base_dir)
            dst_path = os.path.join(dir_path, relative_path)
            
            try:
                if not os.path.exists(dst_path):
                    os.makedirs(dst_path, exist_ok=True)
                shutil.copy2(feature['file_path'], dst_path)  # Use copy2 to preserve metadata
                logging.info(f"Copied file from {src_dir} to {dst_path}.")
            except Exception as e:
                logging.error(f"Failed to copy file from {src_dir} to {dst_path}: {e}")

def analyze_cluster_contents(clusters):
    """
    Analyze cluster contents and generate meaningful names based on file content.
    """
    def get_cluster_summary(features_list):
        content_summary_parts = []
        for feature in features_list:
            content_summary_parts.extend(feature['content'].split()[:50])
        return " ".join(content_summary_parts)

    cluster_names = {}
    for label, features_list in clusters.items():
        summary = get_cluster_summary(features_list)
        name = f"cluster_{label}_{summary[:50].replace(' ', '_')}"
        cluster_names[label] = name
    
    return cluster_names

def get_cluster_name_from_features(features_list):
    """
    Generate a descriptive name for clusters based on common features.
    """
    logging.debug("Generating cluster names based on common features")
    file_operation_count = sum(feature['common_operations']['file_ops'] for feature in features_list)
    class_counts = sum(feature['common_operations']['file_ops'] + feature['common_operations']['subprocess_calls'] for feature in features_list)
    top_import = Counter(feature['imports']).most_common(1)[0][0] if features_list else 'None'

    return f"{file_operation_count}_files_{class_counts}_classes_{top_import}"

def generate_report(clusters):
    """
    Generate a report detailing the contents of each cluster.
    """
    report = {}
    for label, features_list in clusters.items():
        report[label] = {}
        report[label]['cluster_name'] = get_cluster_name_from_features(features_list)
        report[label]['file_summary'] = {
            'total_files': len(features_list),
            'files_with_io': sum(feature['common_operations']['file_ops'] for feature in features_list),
            'files_with_classes': sum(feature['common_operations']['file_ops'] + feature['common_operations']['subprocess_calls'] for feature in features_list),
            'top_import': Counter(feature['imports']).most_common(1)[0][0] if features_list else 'None'
        }
    return report

def rename_clusters(code_clusters_dir, cluster_names):
    """
    Rename cluster directories with generated cluster names.
    """
    logging.debug("Renaming clusters")
    for label, name in cluster_names.items():
        cluster_path = os.path.join(code_clusters_dir, f'cluster_{label}')
        new_cluster_path = os.path.join(code_clusters_dir, name)
        os.rename(cluster_path, new_cluster_path)
        logging.info(f"Renamed {cluster_path} to {new_cluster_path}.")

def dump_report(base_dir, report):
    """
    Dump cluster report into a JSON file.
    """
    logging.debug("Dumping report into JSON file")
    with open(os.path.join(base_dir, 'cluster_report.json'), 'w') as report_file:
        json.dump(report, report_file, indent=4)
    logging.info("Report dumped to JSON file.")

def main():
    """
    Main function to orchestrate the entire process.
    """
    logging.debug("Starting the main process")

    try:
        features_list = []
        # Collect root-level files
        root_level_files = [file for file in Path(base_dir).rglob('*.py') if not any(ignore_dir in str(file) for ignore_dir in ignore_dirs)]
        features_list.extend([parse_python_file(str(file)) for file in root_level_files if parse_python_file(str(file))])

        # Collect from subdirectories
        for root, dirs, files in os.walk(base_dir):
            for dir in dirs:
                full_dir_path = os.path.join(root, dir)
                if not any(ignore_dir in full_dir_path for ignore_dir in ignore_dirs):
                    features_list.extend(extract_features(full_dir_path))
    
        if features_list:
            feature_vectors = generate_feature_vectors(features_list)
            labels = cluster_files(feature_vectors)
            clusters = organize_files(labels, features_list)
            cluster_names = analyze_cluster_contents(clusters)
            
            create_cluster_directories(code_clusters_dir, clusters)
            move_files_to_clusters(base_dir, clusters)
            rename_clusters(code_clusters_dir, cluster_names)
            
            cluster_report = generate_report(clusters)
            dump_report(base_dir, cluster_report)
            
            logging.info("All operations completed successfully.")
        else:
            logging.warning("No Python files found for processing.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    main()
C:\mygit\BLazy\repo\codeorganize\code_classifier_v2.py
Language detected: python
import os
import ast
import astroid
import shutil
import logging
from pathlib import Path
from collections import Counter
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
import numpy as np
import json

# Configure logging
logging.basicConfig(filename='script_log.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

# Define directories
base_dir = r'C:\mygit\BLazy\repo\codeorganize'
ignore_dirs = ['*.venv*', 'cq-gridfinity']
code_clusters_dir = os.path.join(base_dir, 'code_clusters')
os.makedirs(code_clusters_dir, exist_ok=True)


def extract_import_names(node):
    """
    Helper function to extract import names from Import and ImportFrom nodes correctly.
    """
    if isinstance(node, astroid.Import):
        return [(name.name, alias) for name, alias in node.names]
    elif isinstance(node, astroid.ImportFrom):
        return [(node.modname, alias.as_string()) for alias in node.names]
    return []


def resolve_import(module_name, alias=None, context=None):
    try:
        import_module = module_name.split(".")[0]
        return module_name if context.import_module(import_module) else alias if alias else module_name
    except AttributeError:
        return alias if alias else module_name


def parse_python_file(file_path):
    """
    Parse a python file to extract features like imported modules, function/class names, keywords, etc.
    """
    logging.debug(f"Parsing file: {file_path}")
    if not os.path.isfile(file_path) or not file_path.endswith('.py'):
        logging.error(f"Invalid file: {file_path}")
        return None
    
    with open(file_path, 'r') as file:
        content = file.read()
    
    try:
        module_ast = astroid.parse(content, module=file_path)
    except Exception as e:
        logging.error(f"Failed to parse {file_path}: {e}")
        return None
    
    module_ast.file = file_path  # Attach file path to AST for context

    module_imports = []
    for node in module_ast.body:
        if isinstance(node, (astroid.Import, astroid.ImportFrom)):
            module_imports.extend(extract_import_names(node))

    resolved_imports = []
    for module_name, alias in module_imports:
        resolved_name = resolve_import(module_name, alias, module_ast)
        resolved_imports.append(resolved_name)

    module_import_names = sorted(set(resolved_imports))

    class_names = [klass.qname() for klass in module_ast.classes]
    func_names = [func.qname() for func in module_ast.functions]
    keywords_used = [node.keyword for node in module_ast.nodes_of_class(astroid.Keyword)]

    common_operations = {
        'file_ops': ['open', 'read', 'write'],
        'subprocess_calls': ['call', 'run']
    }
    op_counts = Counter()
    
    for node in module_ast.nodes_of_class((astroid.Call, astroid.Assign)):
        if hasattr(node.func, 'name'):
            if any(op in node.func.name for op in common_operations['file_ops']):
                op_counts['file_ops'] += 1
            elif any(op in node.func.name for op in common_operations['subprocess_calls']):
                op_counts['subprocess_calls'] += 1
            
    return {
        'file_path': str(file_path),
        'imports': module_import_names,
        'class_names': class_names,
        'function_names': func_names,
        'keywords': keywords_used,
        'common_operations': dict(op_counts),
        'content': content
    }


def extract_features(directory_path):
    """
    Extract features from all .py files in the given directory.
    """
    logging.debug(f"Extracting features from directory: {directory_path}")
    features_list = []
    if not os.path.isdir(directory_path):
        logging.error(f"Directory does not exist: {directory_path}")
        return features_list
    
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".py") and not any(ignore_dir in root for ignore_dir in ignore_dirs):
                file_path = os.path.join(root, file)
                features = parse_python_file(file_path)
                if features:
                    features_list.append(features)
                    
    return features_list


def generate_feature_vectors(features_list):
    """
    Convert extracted features into a format suitable for clustering.
    """
    logging.debug("Generating feature vectors")
    vectorizer = TfidfVectorizer()
    combined_content = "\n".join(feature['content'] for feature in features_list)
    
    transformed = vectorizer.fit_transform([combined_content])
    feature_names = vectorizer.get_feature_names_out()
    
    feature_vectors = []
    for feature in features_list:
        current_tfidf = vectorizer.transform([feature['content']])
        vector = [current_tfidf.toarray()[0][i] for i in range(len(feature_names))]
        
        file_op_count = feature['common_operations'].get('file_ops', 0)
        subprocess_call_count = feature['common_operations'].get('subprocess_calls', 0)
        feature_vector = [
            len(feature['imports']),
            len(feature['class_names']),
            len(feature['function_names']),
            file_op_count + subprocess_call_count
        ]
        
        vector.extend(feature_vector)
        feature_vectors.append(np.array(vector))
    
    return feature_vectors


def cluster_files(feature_vectors, num_clusters=6):
    """
    Perform clustering using KMeans.
    """
    logging.debug(f"Clustering files with {num_clusters} clusters")
    scaler = StandardScaler()
    scaled_vectors = scaler.fit_transform(feature_vectors)
    
    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(scaled_vectors)
    return kmeans.labels_


def organize_files(labels, features_list):
    """
    Organize files into named clusters.
    """
    clusters = {}
    for label, feature in zip(labels, features_list):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(feature)
    
    return clusters


def create_cluster_directories(code_clusters_dir, clusters):
    """
    Create directories for each cluster.
    """
    logging.debug("Creating cluster directories")
    for label in clusters:
        dir_name = f'cluster_{label}'
        dir_path = os.path.join(code_clusters_dir, dir_name)
        os.makedirs(dir_path, exist_ok=True)


def move_files_to_clusters(base_dir, clusters):
    """
    Copy files to respective cluster directories while maintaining the original file structure.
    """
    logging.debug("Moving files to clusters")
    for label, features_list in clusters.items():
        dir_name = f'cluster_{label}'
        dir_path = os.path.join(code_clusters_dir, dir_name)
        
        for feature in features_list:
            src_dir = os.path.dirname(feature['file_path'])
            relative_path = os.path.relpath(src_dir, base_dir)
            dst_path = os.path.join(dir_path, relative_path)
            
            try:
                if not os.path.exists(dst_path):
                    os.makedirs(dst_path, exist_ok=True)
                shutil.copy2(feature['file_path'], dst_path)  # Use copy2 to preserve metadata
                logging.info(f"Copied file from {src_dir} to {dst_path}.")
            except Exception as e:
                logging.error(f"Failed to copy file from {src_dir} to {dst_path}: {e}")


def analyze_cluster_contents(clusters):
    """
    Analyze cluster contents and generate meaningful names based on file content.
    """
    def get_cluster_summary(features_list):
        content_summary_parts = []
        for feature in features_list:
            content_summary_parts.extend(feature['content'].split()[:50])
        return " ".join(content_summary_parts)

    cluster_names = {}
    for label, features_list in clusters.items():
        summary = get_cluster_summary(features_list)
        name = f"cluster_{label}_{summary[:50].replace(' ', '_')}"
        cluster_names[label] = name
    
    return cluster_names


def get_cluster_name_from_features(features_list):
    """
    Generate a descriptive name for clusters based on common features.
    """
    logging.debug("Generating cluster names based on common features")
    file_operation_count = sum(feature['common_operations']['file_ops'] for feature in features_list)
    class_counts = sum(feature['common_operations']['file_ops'] + feature['common_operations']['subprocess_calls'] for feature in features_list)
    top_import = Counter([item for sublist in [feature['imports'] for feature in features_list] for item in sublist]).most_common(1)[0][0] if features_list else 'None'

    return f"{file_operation_count}_files_{class_counts}_classes_{top_import}"


def generate_report(clusters):
    """
    Generate a report detailing the contents of each cluster.
    """
    report = {}
    for label, features_list in clusters.items():
        report[label] = {}
        report[label]['cluster_name'] = get_cluster_name_from_features(features_list)
        report[label]['file_summary'] = {
            'total_files': len(features_list),
            'files_with_io': sum(feature['common_operations']['file_ops'] for feature in features_list),
            'files_with_classes': sum(
                feature['common_operations']['file_ops'] + feature['common_operations']['subprocess_calls'] for feature in 
                features_list
            ),
            'top_import': Counter([item for sublist in [feature['imports'] for feature in features_list] for item in sublist]).most_common(1)[0][0] if features_list else 'None'
        }
    return report


def rename_clusters(code_clusters_dir, cluster_names):
    """
    Rename cluster directories with generated cluster names.
    """
    logging.debug("Renaming clusters")
    logging.debug(cluster_names)
    for label, name in cluster_names.items():
        cluster_path = os.path.join(code_clusters_dir, f'cluster_{label}')
        new_cluster_path = os.path.join(code_clusters_dir, name)
        os.rename(cluster_path, new_cluster_path)
        logging.info(f"Renamed {cluster_path} to {new_cluster_path}.")


def dump_report(base_dir, report):
    """
    Dump cluster report into a JSON file.
    """
    logging.debug("Dumping report into JSON file")
    with open(os.path.join(base_dir, 'cluster_report.json'), 'w') as report_file:
        json.dump(report, report_file, indent=4)
    logging.info("Report dumped to JSON file.")


def main():
    """
    Main function to orchestrate the entire process.
    """
    logging.debug("Starting the main process")

    try:
        features_list = []
        # Collect root-level files
        root_level_files = [file for file in Path(base_dir).rglob('*.py') if not any(ignore_dir in str(file) for ignore_dir in ignore_dirs)]
        features_list.extend([parse_python_file(str(file)) for file in root_level_files if parse_python_file(str(file))])

        # Collect from subdirectories
        for root, dirs, files in os.walk(base_dir):
            for dir in dirs:
                full_dir_path = os.path.join(root, dir)
                if not any(ignore_dir in full_dir_path for ignore_dir in ignore_dirs):
                    features_list.extend(extract_features(full_dir_path))
    
        if features_list:
            feature_vectors = generate_feature_vectors(features_list)
            labels = cluster_files(feature_vectors)
            clusters = organize_files(labels, features_list)
            cluster_names = analyze_cluster_contents(clusters)
            
            create_cluster_directories(code_clusters_dir, clusters)
            move_files_to_clusters(base_dir, clusters)
            rename_clusters(code_clusters_dir, cluster_names)
            
            cluster_report = generate_report(clusters)
            dump_report(base_dir, cluster_report)
            
            logging.info("All operations completed successfully.")
        else:
            logging.warning("No Python files found for processing.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    main()
C:\mygit\BLazy\repo\codeorganize\code_classifier_v2.py
Language detected: python
import os
import ast
import astroid
import shutil
import logging
from pathlib import Path
from collections import Counter
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
import numpy as np
import json

# Configure logging
logging.basicConfig(filename='script_log.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

# Define directories
base_dir = r'C:\mygit\BLazy\repo\codeorganize'
ignore_dirs = ['*.venv*', 'cq-gridfinity']
code_clusters_dir = os.path.join(base_dir, 'code_clusters')
os.makedirs(code_clusters_dir, exist_ok=True)


def extract_import_names(node):
    """
    Helper function to extract import names from Import and ImportFrom nodes correctly.
    """
    if isinstance(node, astroid.Import):
        return [(name.fullname.split('.')[0], alias) for name, alias in node.names]
    elif isinstance(node, astroid.ImportFrom):
        return [(name.name.split('.')[0], alias.as_string().split('.')[0]) for name, alias in zip(node.modnames, node.names)]
    return []


def parse_python_file(file_path):
    """
    Parse a python file to extract features like imported modules, function/class names, keywords, etc.
    """
    logging.debug(f"Parsing file: {file_path}")
    if not os.path.isfile(file_path) or not file_path.endswith('.py'):
        logging.error(f"Invalid file: {file_path}")
        return None
    
    with open(file_path, 'r') as file:
        content = file.read()
    
    try:
        module_ast = astroid.parse(content, module=str(file_path))
    except Exception as e:
        logging.error(f"Failed to parse {file_path}: {e}")
        return None
    
    module_ast.file = file_path  # Attach file path to AST for context

    module_imports = []
    for node in module_ast.body:
        if isinstance(node, (astroid.Import, astroid.ImportFrom)):
            module_imports.extend(extract_import_names(node))

    module_import_names = sorted(set(item[0] for item in module_imports if item[0]))

    class_names = [klass.qname() for klass in module_ast.classes]
    func_names = [func.qname() for func in module_ast.functions]
    keywords_used = [node.keyword for node in module_ast.nodes_of_class(astroid.Keyword)]

    common_operations = {
        'file_ops': ['open', 'read', 'write'],
        'subprocess_calls': ['call', 'run']
    }
    op_counts = Counter()
    
    for node in module_ast.nodes_of_class((astroid.Call, astroid.Assign)):
        if hasattr(node.func, 'name'):
            if any(op in node.func.name for op in common_operations['file_ops']):
                op_counts['file_ops'] += 1
            elif any(op in node.func.name for op in common_operations['subprocess_calls']):
                op_counts['subprocess_calls'] += 1
            
    return {
        'file_path': str(file_path),
        'imports': module_import_names,
        'class_names': class_names,
        'function_names': func_names,
        'keywords': keywords_used,
        'common_operations': dict(op_counts),
        'content': content
    }


def extract_features(directory_path):
    """
    Extract features from all .py files in the given directory.
    """
    logging.debug(f"Extracting features from directory: {directory_path}")
    features_list = []
    if not os.path.isdir(directory_path):
        logging.error(f"Directory does not exist: {directory_path}")
        return features_list
    
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".py") and not any(ignore_dir in root for ignore_dir in ignore_dirs):
                file_path = os.path.join(root, file)
                features = parse_python_file(file_path)
                if features:
                    features_list.append(features)
                    
    return features_list


def generate_feature_vectors(features_list):
    """
    Convert extracted features into a format suitable for clustering.
    """
    logging.debug("Generating feature vectors")
    vectorizer = TfidfVectorizer()
    combined_content = "\n".join(feature['content'] for feature in features_list)
    
    transformed = vectorizer.fit_transform([combined_content])
    feature_names = vectorizer.get_feature_names_out()
    
    feature_vectors = []
    for feature in features_list:
        current_tfidf = vectorizer.transform([feature['content']])
        vector = [current_tfidf.toarray()[0][i] for i in range(len(feature_names))]
        
        file_op_count = feature['common_operations'].get('file_ops', 0)
        subprocess_call_count = feature['common_operations'].get('subprocess_calls', 0)
        feature_vector = [
            len(feature['imports']),
            len(feature['class_names']),
            len(feature['function_names']),
            file_op_count + subprocess_call_count
        ]
        
        vector.extend(feature_vector)
        feature_vectors.append(np.array(vector))
    
    return feature_vectors


def cluster_files(feature_vectors, num_clusters=6):
    """
    Perform clustering using KMeans.
    """
    logging.debug(f"Clustering files with {num_clusters} clusters")
    scaler = StandardScaler()
    scaled_vectors = scaler.fit_transform(feature_vectors)
    
    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(scaled_vectors)
    return kmeans.labels_


def organize_files(labels, features_list):
    """
    Organize files into named clusters.
    """
    clusters = {}
    for label, feature in zip(labels, features_list):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(feature)
    
    return clusters


def create_cluster_directories(code_clusters_dir, clusters):
    """
    Create directories for each cluster.
    """
    logging.debug("Creating cluster directories")
    for label in clusters:
        dir_name = f'cluster_{label}'
        dir_path = os.path.join(code_clusters_dir, dir_name)
        os.makedirs(dir_path, exist_ok=True)


def move_files_to_clusters(base_dir, clusters):
    """
    Copy files to respective cluster directories while maintaining the original file structure.
    """
    logging.debug("Moving files to clusters")
    for label, features_list in clusters.items():
        dir_name = f'cluster_{label}'
        dir_path = os.path.join(code_clusters_dir, dir_name)
        
        for feature in features_list:
            src_dir = os.path.dirname(feature['file_path'])
            relative_path = os.path.relpath(src_dir, base_dir)
            dst_path = os.path.join(dir_path, relative_path)
            
            try:
                if not os.path.exists(dst_path):
                    os.makedirs(dst_path, exist_ok=True)
                shutil.copy2(feature['file_path'], dst_path)  # Use copy2 to preserve metadata
                logging.info(f"Copied file from {src_dir} to {dst_path}.")
            except Exception as e:
                logging.error(f"Failed to copy file from {src_dir} to {dst_path}: {e}")


def analyze_cluster_contents(clusters):
    """
    Analyze cluster contents and generate meaningful names based on file content.
    """
    def get_cluster_summary(features_list):
        content_summary_parts = []
        for feature in features_list:
            content_summary_parts.extend(feature['content'].split()[:50])
        return " ".join(content_summary_parts)

    cluster_names = {}
    for label, features_list in clusters.items():
        summary = get_cluster_summary(features_list)
        name = f"cluster_{label}_{summary[:50].replace(' ', '_')}"
        cluster_names[label] = name
    
    return cluster_names


def get_cluster_name_from_features(features_list):
    """
    Generate a descriptive name for clusters based on common features.
    """
    logging.debug("Generating cluster names based on common features")
    file_operation_count = sum(feature['common_operations']['file_ops'] for feature in features_list)
    class_counts = sum(len(feature['class_names']) for feature in features_list)
    top_import = Counter([item for sublist in [feature['imports'] for feature in features_list] for item in sublist]).most_common(1)[0][0] if features_list else 'None'

    return f"{file_operation_count}_files_{class_counts}_classes_{top_import}"


def generate_report(clusters):
    """
    Generate a report detailing the contents of each cluster.
    """
    report = {}
    for label, features_list in clusters.items():
        report[label] = {}
        report[label]['cluster_name'] = get_cluster_name_from_features(features_list)
        report[label]['file_summary'] = {
            'total_files': len(features_list),
            'files_with_io': sum(feature['common_operations']['file_ops'] for feature in features_list),
            'files_with_classes': sum(len(feature['class_names']) for feature in features_list),
            'top_import': Counter([item for sublist in [feature['imports'] for feature in features_list] for item in sublist]).most_common(1)[0][0] if features_list else 'None'
        }
    return report


def rename_clusters(code_clusters_dir, cluster_names):
    """
    Rename cluster directories with generated cluster names.
    """
    logging.debug("Renaming clusters")
    logging.debug(cluster_names)
    for label, name in cluster_names.items():
        cluster_path = os.path.join(code_clusters_dir, f'cluster_{label}')
        new_cluster_path = os.path.join(code_clusters_dir, name)
        os.rename(cluster_path, new_cluster_path)
        logging.info(f"Renamed {cluster_path} to {new_cluster_path}.")


def dump_report(base_dir, report):
    """
    Dump cluster report into a JSON file.
    """
    logging.debug("Dumping report into JSON file")
    with open(os.path.join(base_dir, 'cluster_report.json'), 'w') as report_file:
        json.dump(report, report_file, indent=4)
    logging.info("Report dumped to JSON file.")


def main():
    """
    Main function to orchestrate the entire process.
    """
    logging.debug("Starting the main process")

    try:
        features_list = []
        # Collect root-level files
        root_level_files = [file for file in Path(base_dir).rglob('*.py') if not any(ignore_dir in str(file) for ignore_dir in ignore_dirs)]
        features_list.extend([parse_python_file(str(file)) for file in root_level_files if parse_python_file(str(file))])

        # Collect from subdirectories
        for root, dirs, files in os.walk(base_dir):
            for dir in dirs:
                full_dir_path = os.path.join(root, dir)
                if not any(ignore_dir in full_dir_path for ignore_dir in ignore_dirs):
                    features_list.extend(extract_features(full_dir_path))
    
        if features_list:
            feature_vectors = generate_feature_vectors(features_list)
            labels = cluster_files(feature_vectors)
            clusters = organize_files(labels, features_list)
            cluster_names = analyze_cluster_contents(clusters)
            
            create_cluster_directories(code_clusters_dir, clusters)
            move_files_to_clusters(base_dir, clusters)
            rename_clusters(code_clusters_dir, cluster_names)
            
            cluster_report = generate_report(clusters)
            dump_report(base_dir, cluster_report)
            
            logging.info("All operations completed successfully.")
        else:
            logging.warning("No Python files found for processing.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    main()
C:\mygit\BLazy\repo\codeorganize\code_classifier_v2.py
Language detected: python
import os
import ast
import astroid
import shutil
import logging
from pathlib import Path
from collections import Counter
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
import numpy as np
import json

# Configure logging
logging.basicConfig(filename='script_log.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

# Define directories
base_dir = r'C:\mygit\BLazy\repo\codeorganize'
ignore_dirs = ['*.venv*', 'cq-gridfinity']
code_clusters_dir = os.path.join(base_dir, 'code_clusters')
os.makedirs(code_clusters_dir, exist_ok=True)


def extract_import_names(node):
    """
    Helper function to extract import names from Import and ImportFrom nodes safely.
    """
    import_names = set()
    if isinstance(node, (astroid.Import, astroid.ImportFrom)):
        try:
            for name in node.names:
                if isinstance(node, astroid.Import):
                    import_names.add(name[0].fullname.split('.')[0])
                else:  # astroid.ImportFrom
                    import_names.add(name[0].split('.')[0])
        except AttributeError as e:
            logging.error(f"Failed to extract import names from node {node}: {e}")
    return list(import_names)


def parse_python_file(file_path):
    """
    Parse a python file to extract features like imported modules, function/class names, keywords, etc.
    """
    logging.debug(f"Parsing file: {file_path}")
    if not os.path.isfile(file_path) or not file_path.endswith('.py'):
        logging.error(f"Invalid file: {file_path}")
        return None
    
    with open(file_path, 'r') as file:
        content = file.read()
    
    try:
        module_ast = astroid.parse(content, module=str(file_path))
    except Exception as e:
        logging.error(f"Failed to parse {file_path}: {e}")
        return None
    
    module_ast.file = file_path  # Attach file path to AST for context

    module_import_names = extract_import_names(module_ast)
    class_names = [klass.qname() for klass in module_ast.classes]
    func_names = [func.qname() for func in module_ast.functions]
    keywords_used = [node.keyword for node in module_ast.nodes_of_class(astroid.Keyword)]

    common_operations = {
        'file_ops': ['open', 'read', 'write'],
        'subprocess_calls': ['call', 'run']
    }
    op_counts = Counter()
    
    for node in module_ast.nodes_of_class((astroid.Call, astroid.Assign)):
        if hasattr(node.func, 'name'):
            if any(op in node.func.name for op in common_operations['file_ops']):
                op_counts['file_ops'] += 1
            elif any(op in node.func.name for op in common_operations['subprocess_calls']):
                op_counts['subprocess_calls'] += 1
            
    return {
        'file_path': str(file_path),
        'imports': module_import_names,
        'class_names': class_names,
        'function_names': func_names,
        'keywords': keywords_used,
        'common_operations': dict(op_counts),
        'content': content
    }


def extract_features(directory_path):
    """
    Extract features from all .py files in the given directory.
    """
    logging.debug(f"Extracting features from directory: {directory_path}")
    features_list = []
    if not os.path.isdir(directory_path):
        logging.error(f"Directory does not exist: {directory_path}")
        return features_list
    
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".py") and not any(ignore_dir in root for ignore_dir in ignore_dirs):
                file_path = os.path.join(root, file)
                features = parse_python_file(file_path)
                if features:
                    features_list.append(features)
                    
    return features_list


def generate_feature_vectors(features_list):
    """
    Convert extracted features into a format suitable for clustering.
    """
    logging.debug("Generating feature vectors")
    vectorizer = TfidfVectorizer()
    combined_content = "\n".join(feature['content'] for feature in features_list)
    
    transformed = vectorizer.fit_transform([combined_content])
    feature_names = vectorizer.get_feature_names_out()
    
    feature_vectors = []
    for feature in features_list:
        current_tfidf = vectorizer.transform([feature['content']])
        vector = [current_tfidf.toarray()[0][i] for i in range(len(feature_names))]
        
        file_op_count = feature['common_operations'].get('file_ops', 0)
        subprocess_call_count = feature['common_operations'].get('subprocess_calls', 0)
        feature_vector = [
            len(feature['imports']),
            len(feature['class_names']),
            len(feature['function_names']),
            file_op_count + subprocess_call_count
        ]
        
        vector.extend(feature_vector)
        feature_vectors.append(np.array(vector))
    
    return feature_vectors


def cluster_files(feature_vectors, num_clusters=6):
    """
    Perform clustering using KMeans.
    """
    logging.debug(f"Clustering files with {num_clusters} clusters")
    scaler = StandardScaler()
    scaled_vectors = scaler.fit_transform(feature_vectors)
    
    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(scaled_vectors)
    return kmeans.labels_


def organize_files(labels, features_list):
    """
    Organize files into named clusters.
    """
    clusters = {}
    for label, feature in zip(labels, features_list):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(feature)
    
    return clusters


def create_cluster_directories(code_clusters_dir, clusters):
    """
    Create directories for each cluster.
    """
    logging.debug("Creating cluster directories")
    for label in clusters:
        dir_name = f'cluster_{label}'
        dir_path = os.path.join(code_clusters_dir, dir_name)
        os.makedirs(dir_path, exist_ok=True)


def move_files_to_clusters(base_dir, clusters):
    """
    Copy files to respective cluster directories while maintaining the original file structure.
    """
    logging.debug("Moving files to clusters")
    for label, features_list in clusters.items():
        dir_name = f'cluster_{label}'
        dir_path = os.path.join(code_clusters_dir, dir_name)
        
        for feature in features_list:
            src_dir = os.path.dirname(feature['file_path'])
            relative_path = os.path.relpath(src_dir, base_dir)
            dst_path = os.path.join(dir_path, relative_path)
            
            try:
                if not os.path.exists(dst_path):
                    os.makedirs(dst_path, exist_ok=True)
                shutil.copy2(feature['file_path'], dst_path)  # Use copy2 to preserve metadata
                logging.info(f"Copied file from {src_dir} to {dst_path}.")
            except Exception as e:
                logging.error(f"Failed to copy file from {src_dir} to {dst_path}: {e}")


def analyze_cluster_contents(clusters):
    """
    Analyze cluster contents and generate meaningful names based on file content.
    """
    def get_cluster_summary(features_list):
        content_summary_parts = []
        for feature in features_list:
            content_summary_parts.extend(feature['content'].split()[:50])
        return " ".join(content_summary_parts)

    cluster_names = {}
    for label, features_list in clusters.items():
        summary = get_cluster_summary(features_list)
        name = f"cluster_{label}_{summary[:50].replace(' ', '_')}"
        cluster_names[label] = name
    
    return cluster_names


def get_cluster_name_from_features(features_list):
    """
    Generate a descriptive name for clusters based on common features.
    """
    logging.debug("Generating cluster names based on common features")
    file_operation_count = sum(feature['common_operations']['file_ops'] for feature in features_list)
    class_counts = sum(len(feature['class_names']) for feature in features_list)
    top_import = Counter([item for sublist in [feature['imports'] for feature in features_list] for item in sublist]).most_common(1)[0][0] if features_list else 'None'

    return f"{file_operation_count}_files_{class_counts}_classes_{top_import}"


def generate_report(clusters):
    """
    Generate a report detailing the contents of each cluster.
    """
    report = {}
    for label, features_list in clusters.items():
        report[label] = {}
        report[label]['cluster_name'] = get_cluster_name_from_features(features_list)
        report[label]['file_summary'] = {
            'total_files': len(features_list),
            'files_with_io': sum(feature['common_operations']['file_ops'] for feature in features_list),
            'files_with_classes': sum(len(feature['class_names']) for feature in features_list),
            'top_import': Counter([item for sublist in [feature['imports'] for feature in features_list] for item in sublist]).most_common(1)[0][0] if features_list else 'None'
        }
    return report


def rename_clusters(code_clusters_dir, cluster_names):
    """
    Rename cluster directories with generated cluster names.
    """
    logging.debug("Renaming clusters")
    logging.debug(cluster_names)
    for label, name in cluster_names.items():
        cluster_path = os.path.join(code_clusters_dir, f'cluster_{label}')
        new_cluster_path = os.path.join(code_clusters_dir, name)
        os.rename(cluster_path, new_cluster_path)
        logging.info(f"Renamed {cluster_path} to {new_cluster_path}.")


def dump_report(base_dir, report):
    """
    Dump cluster report into a JSON file.
    """
    logging.debug("Dumping report into JSON file")
    with open(os.path.join(base_dir, 'cluster_report.json'), 'w') as report_file:
        json.dump(report, report_file, indent=4)
    logging.info("Report dumped to JSON file.")


def main():
    """
    Main function to orchestrate the entire process.
    """
    logging.debug("Starting the main process")

    try:
        features_list = []
        # Collect root-level files
        root_level_files = [file for file in Path(base_dir).rglob('*.py') if not any(ignore_dir in str(file) for ignore_dir in ignore_dirs)]
        features_list.extend([parse_python_file(str(file)) for file in root_level_files if parse_python_file(str(file))])

        # Collect from subdirectories
        for root, dirs, files in os.walk(base_dir):
            for dir in dirs:
                full_dir_path = os.path.join(root, dir)
                if not any(ignore_dir in full_dir_path for ignore_dir in ignore_dirs):
                    features_list.extend(extract_features(full_dir_path))
    
        if features_list:
            feature_vectors = generate_feature_vectors(features_list)
            labels = cluster_files(feature_vectors)
            clusters = organize_files(labels, features_list)
            cluster_names = analyze_cluster_contents(clusters)
            
            create_cluster_directories(code_clusters_dir, clusters)
            move_files_to_clusters(base_dir, clusters)
            rename_clusters(code_clusters_dir, cluster_names)
            
            cluster_report = generate_report(clusters)
            dump_report(base_dir, cluster_report)
            
            logging.info("All operations completed successfully.")
        else:
            logging.warning("No Python files found for processing.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    main()
C:\mygit\BLazy\repo\codeorganize\code_classifier_v2.py
Language detected: python
import astroid

def safe_get_import_name(node, attr_name):
    """
    Safely retrieve an attribute name from an AST node.
    
    Args:
    node (astroid.NodeNG): The AST node containing the attribute.
    attr_name (str): The attribute name to retrieve.

    Returns:
    str: The attribute name if it exists, otherwise returns 'unknown'.
    """
    try:
        value = getattr(node, attr_name)
        if isinstance(value, str):
            return value
        elif isinstance(value, (tuple, list)):
            return '.'.join([str(val) for val in value])
    except AttributeError:
        pass
    return 'unknown'

def extract_import_names(node):
    """
    Helper function to extract import names from Import and ImportFrom nodes safely.
    """
    import_names = set()
    if isinstance(node, (astroid.Import, astroid.ImportFrom)):
        try:
            for name, alias in node.names:
                if isinstance(node, astroid.Import):
                    full_name = safe_get_import_name(node, 'modname')
                    module_name = safe_get_import_name(alias or name, 'name')
                    import_names.add('{}.{}'.format(full_name, module_name).split('.')[0])
                else:  # astroid.ImportFrom
                    module_name = node.modname or ''
                    import_names.add('{}.{}'.format(module_name, name).split('.')[0])
        except Exception as e:
            logging.error(f"Failed to extract import names from node {node}: {e}")
    return list(import_names)

# Existing code remains unchanged...
C:\mygit\BLazy\repo\codeorganize\code_classifier_v2.py
Language detected: python
# Required imports
import os
import astroid
import shutil
import logging
from collections import Counter
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
import numpy as np

# Configure logging
logging.basicConfig(filename='script_log.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Define directories
base_dir = r'C:\mygit\BLazy\repo\codeorganize\llm_gen_code'
directories = ['directory_operations', 'subprocess_operations']

def parse_python_file(file_path):
    """
    Parse a python file to extract features like imported modules, function/class names, keywords, etc.
    """
    if not os.path.isfile(file_path) or not file_path.endswith('.py'):
        logging.error(f"Invalid file: {file_path}")
        return None
    
    with open(file_path, 'r') as file:
        content = file.read()
    
    try:
        module_ast = astroid.parse(content)
    except Exception as e:
        logging.error(f"Failed to parse {file_path}: {e}")
        return None
    
    imports = extract_import_names(module_ast)
    class_names = [klass.name for klass in module_ast.classes]
    func_names = [func.name for func in module_ast.functions]
    keywords_used = [node.keyword for node in module_ast.nodes_of_class(astroid.Keyword)]

    common_operations = {
        'file_ops': ['open', 'read', 'write'],
        'subprocess_calls': ['call', 'run']
    }
    op_counts = Counter()
    
    for node in module_ast.nodes_of_class((astroid.Call, astroid.Assign)):
        if hasattr(node.func, 'name'):
            if any(op in node.func.name for op in common_operations['file_ops']):
                op_counts['file_ops'] += 1
            elif any(op in node.func.name for op in common_operations['subprocess_calls']):
                op_counts['subprocess_calls'] += 1
            
    return {
        'file_path': file_path,
        'imports': imports,
        'class_names': class_names,
        'function_names': func_names,
        'keywords': keywords_used,
        'common_operations': dict(op_counts),
        'content': content
    }

def extract_import_names(node):
    """
    Extract import names from given AST node.
    """
    import_names = set()
    if isinstance(node, (astroid.Import, astroid.ImportFrom)):
        try:
            for name, alias in node.names:
                if isinstance(node, astroid.Import):
                    full_name = safe_get_import_name(node, 'modname')
                    module_name = safe_get_import_name(alias or name, 'name')
                    import_names.add('{}.{}'.format(full_name, module_name))
                else:  # astroid.ImportFrom
                    module_name = node.modname or ''
                    import_names.add('{}.{}'.format(module_name, name))
        except Exception as e:
            logging.error(f"Failed to extract import names from node {node}: {e}")
    return list(import_names)

def safe_get_import_name(node, attr_name):
    """
    Safely retrieve an attribute name from an AST node.
    
    Args:
    node (astroid.NodeNG): The AST node containing the attribute.
    attr_name (str): The attribute name to retrieve.

    Returns:
    str: The attribute name if it exists, otherwise returns 'unknown'.
    """
    try:
        value = getattr(node, attr_name)
        if isinstance(value, str):
            return value
        elif isinstance(value, (tuple, list)):
            return '.'.join([str(val) for val in value])
    except AttributeError:
        pass
    return 'unknown'

def extract_features(directory_path):
    """
    Extract features from all .py files in the given directory.
    """
    features_list = []
    if not os.path.isdir(directory_path):
        logging.error(f"Directory does not exist: {directory_path}")
        return features_list
    
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                features = parse_python_file(file_path)
                if features:
                    features_list.append(features)
    
    return features_list

def generate_feature_vectors(features_list):
    """
    Convert extracted features into a format suitable for clustering.
    """
    vectorizer = TfidfVectorizer()
    combined_content = "\n".join(feature['content'] for feature in features_list)
    
    transformed = vectorizer.fit_transform([combined_content])
    feature_names = vectorizer.get_feature_names_out()
    
    feature_vectors = []
    for feature in features_list:
        current_tfidf = vectorizer.transform([feature['content']])
        vector = [current_tfidf.toarray()[0][i] if any(word in feature['content'] for word in feature_names) else 0 for i in range(len(feature_names))]
        feature_vector = [
            len(feature['imports']), len(feature['class_names']), len(feature['function_names']),
            sum(feature['common_operations'].get('file_ops', 0) + feature['common_operations'].get('subprocess_calls', 0)),
        ]
        
        vector.extend(feature_vector)
        feature_vectors.append(np.array(vector))
    
    return np.array(feature_vectors)

def cluster_files(feature_vectors, num_clusters=3):
    """
    Perform clustering using KMeans.
    """
    scaler = StandardScaler()
    scaled_vectors = scaler.fit_transform(feature_vectors)
    
    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(scaled_vectors)
    return kmeans.labels_

def organize_files(labels, features_list):
    """
    Organize files into named clusters.
    """
    clusters = {}
    for label, feature in zip(labels, features_list):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(feature)
    
    return clusters

def validate_input_directories(directories):
    """
    Validate input directories.
    """
    valid_directories = []
    for directory in directories:
        directory_path = os.path.join(base_dir, directory)
        if os.path.isdir(directory_path):
            valid_directories.append(directory_path)
        else:
            logging.error(f"Directory does not exist: {directory_path}")
    
    return valid_directories

def create_cluster_directories(base_dir, clusters):
    """
    Create directories for each cluster.
    """
    for label in clusters:
        dir_name = f'cluster_{label}'
        dir_path = os.path.join(base_dir, dir_name)
        os.makedirs(dir_path, exist_ok=True)

def move_files_to_clusters(base_dir, clusters):
    """
    Move files to respective cluster directories while preserving original file structure.
    """
    for label, features_list in clusters.items():
        dir_name = f'cluster_{label}'
        dir_path = os.path.join(base_dir, dir_name)
        
        for feature in features_list:
            src_dir = os.path.dirname(feature['file_path'])
            relative_path = os.path.relpath(src_dir, base_dir)
            dst_path = os.path.join(dir_path, relative_path)
            
            try:
                if not os.path.exists(dst_path):
                    os.makedirs(dst_path, exist_ok=True)
                shutil.move(feature['file_path'], dst_path)
                logging.info(f"Moved file from {src_dir} to {dst_path}.")
            except Exception as e:
                logging.error(f"Failed to move file from {src_dir} to {dst_path}: {e}")

def analyze_cluster_contents(clusters):
    """
    Analyze cluster contents and generate meaningful names based on file content.
    """
    cluster_names = {}
    for label, features_list in clusters.items():
        content_summary = " ".join(feature['content'][:100] for feature in features_list)
        name = f"cluster_{label}_{content_summary[:10]}"
        cluster_names[label] = name
    
    return cluster_names

def main():
    """
    Main function to orchestrate the entire process.
    """
    validated_directories = validate_input_directories(directories)
    features_list = []
    for directory in validated_directories:
        features_list.extend(extract_features(directory))
        backup_dir = os.path.join(base_dir, f'backup_{os.path.basename(directory)}')
        os.makedirs(backup_dir, exist_ok=True)
        shutil.copytree(directory, backup_dir, dirs_exist_ok=True)
        logging.info(f"Backup created for {directory}.")
    
    if features_list:
        feature_vectors = generate_feature_vectors(features_list)
        labels = cluster_files(feature_vectors)
        clusters = organize_files(labels, features_list)
        cluster_names = analyze_cluster_contents(clusters)
        
        create_cluster_directories(base_dir, clusters)
        move_files_to_clusters(base_dir, clusters)
        
        for label, name in cluster_names.items():
            os.rename(os.path.join(base_dir, f'cluster_{label}'), os.path.join(base_dir, name))
            logging.info(f"Renamed {label} to {name}.")
        
        logging.info("All operations completed successfully.")
    else:
        logging.warning("No Python files found for processing.")

if __name__ == "__main__":
    main()
