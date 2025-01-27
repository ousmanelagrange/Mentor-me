import numpy as np

class AHP:
    """
    Cette classe implémente le processus d'Analyse Hiérarchique par Processus (AHP).
    """

    def __init__(self, pair_wise_comparison_matrix):
        """
        Initialise la classe AHP avec la matrice de comparaison par paires.
        
        Parameters:
        pair_wise_comparison_matrix (numpy.ndarray): La matrice de comparaison par paires.
        """
        self.pair_wise_comparison_matrix = pair_wise_comparison_matrix

    def calacul_normalize_pair_wise_matrix(self):
        """
        Calcule la matrice de comparaison par paires normalisée.
        
        Returns:
        numpy.ndarray: La matrice de comparaison par paires normalisée.
        """
        normalized_pair_wise_matrix = self.pair_wise_comparison_matrix.copy()
        for index, cell in np.ndenumerate(self.pair_wise_comparison_matrix):
            sum = np.array([row[index[1]] for row in self.pair_wise_comparison_matrix]).sum()
            normalized_pair_wise_matrix[index[0], index[1]] = cell / sum
        self.normalize_pair_wise_matrix = normalized_pair_wise_matrix
        return normalized_pair_wise_matrix
    
    def calculate_criterial_weights(self):
        """
        Calcule les poids des critères à partir de la matrice normalisée.
        
        Returns:
        numpy.ndarray: Les poids des critères.
        """
        n = self.normalize_pair_wise_matrix.shape[1]
        self.criterial_weights = np.array([row.sum() / n for row in self.normalize_pair_wise_matrix])
        return self.criterial_weights
    
    def calculate_criteria_weighted_sum(self):
        """
        Calcule la somme pondérée des critères.
        
        Returns:
        numpy.ndarray: La somme pondérée des critères.
        """
        pair_wise_comparison_matrix_edited = self.pair_wise_comparison_matrix.copy()
        criterial_weights = self.criterial_weights

        for index, cell in np.ndenumerate(self.pair_wise_comparison_matrix):
            pair_wise_comparison_matrix_edited[index[0], index[1]] = cell * criterial_weights[index[1]]
        self.criteria_weighted_sum = np.array([row.sum() for row in pair_wise_comparison_matrix_edited])
        return self.criteria_weighted_sum

    def calculate_lambda_i(self):
        """
        Calcule les valeurs propres (lambda_i).
        
        Returns:
        numpy.ndarray: Les valeurs propres (lambda_i).
        """
        criterial_weights = self.criterial_weights.copy()
        criteria_weighted_sum = self.criteria_weighted_sum.copy()
        self.lambda_i = criteria_weighted_sum / criterial_weights
        return self.lambda_i
    
    def calculate_lambda_max(self):
        """
        Calcule la valeur propre maximale (lambda_max).
        
        Returns:
        float: La valeur propre maximale (lambda_max).
        """
        lambda_i = self.lambda_i.copy()
        self.lambda_max = lambda_i.sum() / lambda_i.shape[0]
        return self.lambda_max
    
    def calculate_consistency_index(self):
        """
        Calcule l'indice de cohérence (CI).
        
        Returns:
        float: L'indice de cohérence (CI).
        """
        lambda_max = self.lambda_max.copy()
        n = self.lambda_i.shape[0]
        self.consistency_index = (lambda_max - n) / (n - 1)
        return self.consistency_index

    def calculate_consistency_ration(self):
        """
        Calcule le ratio de cohérence (CR).
        
        Returns:
        float: Le ratio de cohérence (CR).
        """
        n = self.lambda_i.shape[0]
        ci = self.consistency_index.copy()
        ri = np.array([0.00, 0.00, 0.58, 0.90, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49, 1.51, 1.48, 1.56, 1.57, 1.59])
        self.consistency_ration = ci / ri[n - 1]
        return self.consistency_ration

    def run(self):
        """
        Exécute l'ensemble du processus AHP.
        
        Returns:
        dict: Les résultats du processus AHP comprenant les matrices et les indices calculés.
        """
        self.calacul_normalize_pair_wise_matrix()
        self.calculate_criterial_weights()
        self.calculate_criteria_weighted_sum()
        self.calculate_lambda_i()
        self.calculate_lambda_max()
        self.calculate_consistency_index()
        self.calculate_consistency_ration()

        res = {
            "pair_wise_comparison_matrix": self.pair_wise_comparison_matrix,
            "normalize_pair_wise_matrix": self.normalize_pair_wise_matrix,
            "criterial_weights": self.criterial_weights,
            "criteria_weighted_sum": self.criteria_weighted_sum,
            "lambda_i": self.lambda_i,
            "lambda_max": self.lambda_max,
            "consistency_index": self.consistency_index,
            "consistency_ration": self.consistency_ration
        }

        return res
    
    def select_best_alternative(self, alternative):
        """
        Sélectionne la meilleure alternative en fonction des poids des critères.

        Parameters:
        alternative (dict): Un dictionnaire contenant les matrices alternatives et les noms des alternatives.
                            - "alternative_matrices" (numpy.ndarray): Une matrice où chaque ligne représente une alternative
                            et chaque colonne représente un critère.
                            - "name" (list): Une liste de noms correspondant aux alternatives.

        Returns:
        str: Une chaîne de caractères indiquant la meilleure alternative.
        """
        # Récupère la matrice des alternatives
        alt = alternative["alternative_matrices"]

        # Multiplie chaque élément de la matrice des alternatives par le poids correspondant du critère
        for index, cell in np.ndenumerate(alt):
            alt[index[0], index[1]] = cell * self.criterial_weights[index[1]]

        # Calcule la somme pondérée pour chaque alternative
        total_item_weight = np.array([row.sum() for row in alt])

        # Initialise l'index de la meilleure alternative
        index = 0

        # Trouve l'index de l'alternative avec la somme pondérée maximale
        for id, cell in np.ndenumerate(total_item_weight):
            if cell == total_item_weight.max():
                index = id[0]
                break

        # Récupère le nom de la meilleure alternative
        best_alternative = alternative["name"][index]

        # Retourne une chaîne indiquant la meilleure alternative
        return f"The best alternative is: {best_alternative}"

    def get_weights(self):
        self.calacul_normalize_pair_wise_matrix()
        self.calculate_criterial_weights()
        return {
            "expertise_similarity":self.criterial_weights[0],
            "qualification_compatibility":self.criterial_weights[1],
            "experience_relevance":self.criterial_weights[2],
            "common_language":self.criterial_weights[3],
            "availability":self.criterial_weights[4],
            "mentorship_preferences":self.criterial_weights[5]
            
        }
        
    
    def __str__(self):
        """
        Retourne une chaîne de caractères représentant les résultats du processus AHP.
        
        Returns:
        str: La représentation en chaîne de caractères des résultats du processus AHP.
        """
        self.calacul_normalize_pair_wise_matrix()
        self.calculate_criterial_weights()
        self.calculate_criteria_weighted_sum()
        self.calculate_lambda_i()
        self.calculate_lambda_max()
        self.calculate_consistency_index()
        self.calculate_consistency_ration()

        return f"""AHP:\n pair wise comparison matrix: \n{self.pair_wise_comparison_matrix}\n normalize pair wise matrix:\n {self.normalize_pair_wise_matrix}\n criterial weights: {self.criterial_weights}\n criteria weighted_sum: {self.criteria_weighted_sum}\n lambda_i: {self.lambda_i}\n lambda_max: {self.lambda_max}\n consistency_index:{self.consistency_index}\n consistency_ration: {self.consistency_ration}"""
