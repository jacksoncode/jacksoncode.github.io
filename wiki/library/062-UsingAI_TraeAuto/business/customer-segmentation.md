# AI客户细分

## 基本原理
AI客户细分是利用人工智能技术将客户群体划分为具有相似特征的子群体的过程。它通过分析客户的人口统计信息、购买历史、行为模式、偏好等多维度数据，识别出不同的客户群体，帮助企业制定精准的营销策略、个性化服务和产品推荐。

### 技术方法
AI客户细分常用的技术方法包括：
1. **无监督学习算法**：如K-means聚类、层次聚类、DBSCAN等
2. **监督学习算法**：如决策树、随机森林、支持向量机等（当有已知类别标签时）
3. **深度学习模型**：如自编码器、变分自编码器等
4. **混合模型**：结合多种算法的优势
5. **降维技术**：如PCA、t-SNE、UMAP等（用于数据可视化和特征提取）

### 核心原理
AI客户细分的核心原理包括：
1. **相似性度量**：基于客户特征计算客户间的相似性或距离
2. **聚类分析**：将相似的客户聚为一类
3. **特征重要性评估**：识别对客户细分最有影响力的特征
4. **模型评估与优化**：通过评估指标选择最优的聚类模型
5. **结果解释与应用**：将聚类结果转化为可操作的商业洞见

### 常用模型
- **K-means聚类**：适合大规模数据的快速聚类，假设类簇是球形的
- **层次聚类**：适合构建客户的层次结构，不需要预先指定聚类数量
- **DBSCAN**：适合发现任意形状的类簇，能够处理噪声和离群点
- **高斯混合模型(GMM)**：适合处理混合分布的数据
- **自编码器(Autoencoder)**：适合处理高维数据，能够学习数据的潜在表示

## 应用场景
AI客户细分在企业中有广泛的应用场景：

### 1. 精准营销
根据不同客户群体的特征和偏好，制定针对性的营销策略，提高营销效果和ROI。

### 2. 个性化推荐
基于客户群体的购买历史和偏好，提供个性化的产品或服务推荐，提升客户体验和销售额。

### 3. 客户价值评估
识别高价值客户、潜在流失客户和低价值客户，优化资源分配和客户关系管理。

### 4. 产品开发
基于不同客户群体的需求，开发满足特定群体需求的产品或服务，提高产品成功率。

### 5. 客户生命周期管理
根据客户在生命周期中的不同阶段，制定相应的客户管理策略，延长客户生命周期。

### 6. 定价策略
针对不同客户群体的价格敏感度，制定差异化的定价策略，最大化利润和市场份额。

### 7. 渠道优化
根据不同客户群体的渠道偏好，优化渠道配置和资源分配，提高渠道效率。

### 8. 客户体验优化
识别不同客户群体的痛点和需求，优化客户体验，提高客户满意度和忠诚度。

## 基础示例：使用Python实现AI客户细分
下面是一个使用Python实现的基础AI客户细分系统示例，包含数据加载、预处理、聚类分析和结果可视化功能。

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from scipy.cluster.hierarchy import dendrogram, linkage
import warnings
warnings.filterwarnings('ignore')

class AICustomerSegmentation:
    """
    基础AI客户细分系统
    """
    def __init__(self):
        """
        初始化客户细分器
        """
        self.models = {
            'KMeans': KMeans(random_state=42),
            'Hierarchical': AgglomerativeClustering(),
            'DBSCAN': DBSCAN()
        }
        self.best_model = None
        self.data = None
        self.raw_data = None
        self.scaler = StandardScaler()
        self.cluster_labels = None
        self.metrics = {}
        
    def load_data(self, file_path=None, sample_data=True, n_samples=500):
        """
        加载客户数据
        """
        if sample_data:
            # 生成样本客户数据
            np.random.seed(42)
            
            # 客户特征
            age = np.random.randint(18, 70, n_samples)
            income = np.random.normal(50000, 20000, n_samples)  # 年收入
            income = np.maximum(income, 20000)  # 确保收入不低于20000
            
            # 购买行为特征
            purchase_frequency = np.random.exponential(0.5, n_samples) * 12  # 年购买频率
            avg_purchase_value = income * np.random.uniform(0.01, 0.1, n_samples)  # 平均购买价值
            total_spend = purchase_frequency * avg_purchase_value  # 总消费
            
            # 客户忠诚度特征
            membership_years = np.random.randint(0, 10, n_samples)  # 会员年限
            churn_risk = np.exp(-0.3 * membership_years) * np.random.uniform(0.1, 0.5, n_samples)  # 流失风险
            
            # 客户满意度
            satisfaction_score = np.random.normal(4, 0.8, n_samples)  # 满意度得分
            satisfaction_score = np.clip(satisfaction_score, 1, 5)  # 限制在1-5之间
            
            # 创建DataFrame
            self.raw_data = pd.DataFrame({
                'customer_id': [f'CUST{i:04d}' for i in range(1, n_samples+1)],
                'age': age,
                'income': income,
                'purchase_frequency': purchase_frequency,
                'avg_purchase_value': avg_purchase_value,
                'total_spend': total_spend,
                'membership_years': membership_years,
                'churn_risk': churn_risk,
                'satisfaction_score': satisfaction_score
            })
            
            # 复制原始数据用于分析
            self.data = self.raw_data.copy()
        else:
            # 从文件加载数据
            if file_path is None:
                raise ValueError("如果不使用样本数据，必须提供文件路径")
            
            # 假设CSV文件包含必要的列
            self.raw_data = pd.read_csv(file_path)
            self.data = self.raw_data.copy()
        
        return self.data
    
    def data_preprocessing(self, feature_columns=None, scaling_method='standard'):
        """
        预处理客户数据
        """
        if self.data is None:
            raise ValueError("请先加载数据")
        
        # 如果未指定特征列，使用所有数值型列（除了客户ID）
        if feature_columns is None:
            feature_columns = [col for col in self.data.columns 
                              if col != 'customer_id' and self.data[col].dtype in ['int64', 'float64']]
        
        # 选择特征
        X = self.data[feature_columns].copy()
        
        # 处理缺失值
        X.fillna(X.mean(), inplace=True)
        
        # 特征缩放
        if scaling_method == 'standard':
            self.scaler = StandardScaler()
        elif scaling_method == 'minmax':
            self.scaler = MinMaxScaler()
        else:
            raise ValueError("不支持的缩放方法")
        
        X_scaled = self.scaler.fit_transform(X)
        
        # 将缩放后的数据转换回DataFrame
        X_scaled_df = pd.DataFrame(X_scaled, columns=feature_columns, index=X.index)
        
        return X_scaled_df, feature_columns
    
    def determine_optimal_clusters(self, X, max_clusters=10):
        """
        确定最优聚类数量（仅适用于K-means等需要预先指定聚类数量的算法）
        """
        # 肘部法则
        wcss = []  # 簇内平方和
        silhouette_scores = []
        
        for k in range(2, max_clusters + 1):
            kmeans = KMeans(n_clusters=k, random_state=42)
            kmeans.fit(X)
            wcss.append(kmeans.inertia_)
            silhouette_scores.append(silhouette_score(X, kmeans.labels_))
        
        # 可视化肘部法则
        plt.figure(figsize=(12, 5))
        
        plt.subplot(1, 2, 1)
        plt.plot(range(2, max_clusters + 1), wcss, marker='o')
        plt.title('肘部法则确定最优聚类数量')
        plt.xlabel('聚类数量')
        plt.ylabel('WCSS (簇内平方和)')
        plt.grid(True)
        
        plt.subplot(1, 2, 2)
        plt.plot(range(2, max_clusters + 1), silhouette_scores, marker='o')
        plt.title('轮廓系数确定最优聚类数量')
        plt.xlabel('聚类数量')
        plt.ylabel('轮廓系数')
        plt.grid(True)
        
        plt.tight_layout()
        plt.show()
        
        # 选择轮廓系数最大的聚类数量
        optimal_k = 2 + silhouette_scores.index(max(silhouette_scores))
        print(f"最优聚类数量: {optimal_k}")
        
        return optimal_k
    
    def perform_clustering(self, X, algorithm='KMeans', n_clusters=4, **kwargs):
        """
        执行客户聚类
        """
        if algorithm not in self.models:
            raise ValueError(f"不支持的聚类算法: {algorithm}")
        
        # 根据算法设置参数
        if algorithm == 'KMeans':
            model = KMeans(n_clusters=n_clusters, random_state=42, **kwargs)
        elif algorithm == 'Hierarchical':
            model = AgglomerativeClustering(n_clusters=n_clusters, **kwargs)
        elif algorithm == 'DBSCAN':
            model = DBSCAN(**kwargs)
        
        # 执行聚类
        self.cluster_labels = model.fit_predict(X)
        
        # 保存最佳模型
        self.best_model = model
        
        print(f"使用{algorithm}算法完成客户聚类")
        
        # 统计每个簇的客户数量
        unique_labels, counts = np.unique(self.cluster_labels, return_counts=True)
        print("各簇客户数量:")
        for label, count in zip(unique_labels, counts):
            print(f"簇 {label}: {count} 个客户 ({count/len(X)*100:.2f}%)")
        
        return self.cluster_labels
    
    def evaluate_clustering(self, X):
        """
        评估聚类结果
        """
        if self.cluster_labels is None:
            raise ValueError("请先执行聚类")
        
        # 计算评估指标
        n_clusters = len(np.unique(self.cluster_labels))
        
        # 只有当聚类数量大于1且小于样本数量时才能计算这些指标
        if n_clusters > 1 and n_clusters < len(X):
            try:
                silhouette_avg = silhouette_score(X, self.cluster_labels)
                db_score = davies_bouldin_score(X, self.cluster_labels)
                ch_score = calinski_harabasz_score(X, self.cluster_labels)
                
                self.metrics = {
                    'Silhouette Score': silhouette_avg,
                    'Davies-Bouldin Score': db_score,
                    'Calinski-Harabasz Score': ch_score,
                    'Number of Clusters': n_clusters
                }
                
                print("聚类评估指标:")
                print(f"轮廓系数: {silhouette_avg:.4f} (越接近1越好)")
                print(f"Davies-Bouldin指数: {db_score:.4f} (值越小越好)")
                print(f"Calinski-Harabasz指数: {ch_score:.4f} (值越大越好)")
            except Exception as e:
                print(f"评估聚类结果时出错: {e}")
        else:
            print("聚类数量不合适，无法计算评估指标")
        
        return self.metrics
    
    def visualize_clusters(self, X, feature_columns, method='pca'):
        """
        可视化聚类结果
        """
        if self.cluster_labels is None:
            raise ValueError("请先执行聚类")
        
        # 降维以便可视化
        if method == 'pca' and X.shape[1] > 2:
            pca = PCA(n_components=2)
            X_reduced = pca.fit_transform(X)
            print(f"PCA降维保留的方差比例: {sum(pca.explained_variance_ratio_):.4f}")
        else:
            # 如果特征数量小于等于2，直接使用前两个特征
            X_reduced = X.iloc[:, :2].values
        
        # 可视化聚类结果
        plt.figure(figsize=(10, 8))
        scatter = plt.scatter(X_reduced[:, 0], X_reduced[:, 1], 
                             c=self.cluster_labels, cmap='viridis', s=50, alpha=0.7)
        plt.title('客户聚类结果可视化')
        plt.xlabel('特征1')
        plt.ylabel('特征2')
        plt.colorbar(scatter, label='聚类标签')
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        
        # 对于层次聚类，绘制树状图
        if isinstance(self.best_model, AgglomerativeClustering):
            plt.figure(figsize=(12, 8))
            Z = linkage(X, 'ward')
            dendrogram(Z, truncate_mode='lastp', p=10, leaf_rotation=45., leaf_font_size=15.)
            plt.title('层次聚类树状图')
            plt.xlabel('样本')
            plt.ylabel('距离')
            plt.tight_layout()
            plt.show()
    
    def analyze_cluster_profiles(self, feature_columns):
        """
        分析每个簇的特征概况
        """
        if self.cluster_labels is None:
            raise ValueError("请先执行聚类")
        
        # 将聚类标签添加到原始数据中
        result_data = self.raw_data.copy()
        result_data['cluster'] = self.cluster_labels
        
        # 计算每个簇的特征均值
        cluster_profiles = result_data.groupby('cluster')[feature_columns].mean()
        
        print("\n各簇特征概况:")
        print(cluster_profiles)
        
        # 可视化每个簇的特征分布
        n_features = len(feature_columns)
        n_clusters = len(cluster_profiles)
        
        fig, axes = plt.subplots(n_features, 1, figsize=(12, 3 * n_features))
        
        for i, feature in enumerate(feature_columns):
            for cluster in range(n_clusters):
                cluster_data = result_data[result_data['cluster'] == cluster][feature]
                sns.kdeplot(cluster_data, ax=axes[i], label=f'簇 {cluster}')
            axes[i].set_title(f'{feature}的簇间分布')
            axes[i].set_xlabel(feature)
            axes[i].set_ylabel('密度')
            axes[i].legend()
            axes[i].grid(True)
        
        plt.tight_layout()
        plt.show()
        
        # 热力图展示各簇特征对比
        plt.figure(figsize=(12, 8))
        sns.heatmap(cluster_profiles.T, annot=True, cmap='YlGnBu')
        plt.title('各簇特征均值对比')
        plt.tight_layout()
        plt.show()
        
        return cluster_profiles
    
    def generate_segmentation_report(self, feature_columns):
        """
        生成客户细分报告
        """
        if self.cluster_labels is None:
            raise ValueError("请先执行聚类")
        
        # 分析簇概况
        cluster_profiles = self.analyze_cluster_profiles(feature_columns)
        
        # 为每个簇生成描述性标签
        segment_labels = {}
        n_clusters = len(cluster_profiles)
        
        for cluster in range(n_clusters):
            # 这里使用简单的规则生成标签，实际应用中可能需要更复杂的逻辑
            profile = cluster_profiles.loc[cluster]
            
            # 基于关键特征生成标签
            if 'total_spend' in profile and 'purchase_frequency' in profile:
                spend_rank = profile['total_spend'].rank(ascending=False)
                freq_rank = profile['purchase_frequency'].rank(ascending=False)
                
                if spend_rank <= 2 and freq_rank <= 2:
                    segment_labels[cluster] = '高价值活跃客户'
                elif spend_rank <= 2 and freq_rank > 2:
                    segment_labels[cluster] = '高价值低活跃客户'
                elif spend_rank > 2 and freq_rank <= 2:
                    segment_labels[cluster] = '低价值活跃客户'
                else:
                    segment_labels[cluster] = '低价值低活跃客户'
            else:
                segment_labels[cluster] = f'客户群体{cluster+1}'
        
        # 统计每个段的客户数量
        segment_counts = pd.Series(self.cluster_labels).value_counts().sort_index()
        
        print("\n===== 客户细分报告 =====")
        for cluster in range(n_clusters):
            count = segment_counts[cluster]
            percentage = count / len(self.cluster_labels) * 100
            print(f"\n{segment_labels[cluster]} (簇 {cluster}):")
            print(f"  客户数量: {count} ({percentage:.2f}%)")
            print("  特征概况:")
            for feature in feature_columns:
                print(f"    {feature}: {cluster_profiles.loc[cluster, feature]:.2f}")
        print("====================")
        
        return {
            'segment_labels': segment_labels,
            'segment_counts': segment_counts,
            'cluster_profiles': cluster_profiles
        }

# 使用示例
if __name__ == "__main__":
    # 创建AI客户细分器实例
    customer_segmenter = AICustomerSegmentation()
    
    print("正在初始化AI客户细分系统...")
    
    # 加载样本数据
    print("\n加载样本客户数据...")
    customer_segmenter.load_data(sample_data=True, n_samples=500)
    print(f"数据加载完成，共有{len(customer_segmenter.data)}个客户记录")
    
    # 数据预处理
    print("\n预处理客户数据...")
    feature_columns = ['age', 'income', 'purchase_frequency', 'avg_purchase_value', 
                      'total_spend', 'membership_years', 'satisfaction_score']
    X_scaled, selected_features = customer_segmenter.data_preprocessing(feature_columns)
    print(f"预处理完成，使用的特征: {selected_features}")
    
    # 确定最优聚类数量
    print("\n确定最优聚类数量...")
    optimal_k = customer_segmenter.determine_optimal_clusters(X_scaled, max_clusters=8)
    
    # 执行客户聚类
    print("\n执行客户聚类...")
    cluster_labels = customer_segmenter.perform_clustering(X_scaled, algorithm='KMeans', n_clusters=optimal_k)
    
    # 评估聚类结果
    print("\n评估聚类结果...")
    metrics = customer_segmenter.evaluate_clustering(X_scaled)
    
    # 可视化聚类结果
    print("\n可视化聚类结果...")
    customer_segmenter.visualize_clusters(X_scaled, selected_features)
    
    # 分析簇概况
    print("\n分析各簇特征概况...")
    cluster_profiles = customer_segmenter.analyze_cluster_profiles(selected_features)
    
    # 生成客户细分报告
    print("\n生成客户细分报告...")
    report = customer_segmenter.generate_segmentation_report(selected_features)
    
    print("\nAI客户细分系统运行完成！")
```

## 高级示例：使用Python实现高级AI客户细分系统
下面是一个更高级的AI客户细分系统实现，包含了更多高级功能，如多模型集成、深度学习聚类、客户生命周期价值预测和动态细分等。

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.decomposition import PCA, KernelPCA, FastICA
from sklearn.manifold import TSNE, UMAP
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.layers import Input, Dense, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam
from scipy.cluster.hierarchy import dendrogram, linkage
from lifetimes import BetaGeoFitter, GammaGammaFitter
from lifetimes.plotting import plot_frequency_recency_matrix, plot_probability_alive_matrix
import warnings
warnings.filterwarnings('ignore')

class AdvancedAICustomerSegmentation:
    """
    高级AI客户细分系统
    """
    def __init__(self):
        """
        初始化高级客户细分器
        """
        # 定义更多聚类模型
        self.models = {
            'KMeans': KMeans(random_state=42),
            'GaussianMixture': GaussianMixture(random_state=42),
            'Hierarchical': AgglomerativeClustering(),
            'DBSCAN': DBSCAN(),
        }
        self.best_model = None
        self.data = None
        self.raw_data = None
        self.scaler = StandardScaler()
        self.cluster_labels = None
        self.metrics = {}
        self.autoencoder = None
        self.customer_lifetime_value = None

    def load_data(self, file_path=None, sample_data=True, n_samples=1000):
        """
        加载更丰富的客户数据
        """
        if sample_data:
            # 生成更复杂的样本客户数据
            np.random.seed(42)
            
            # 基础客户信息
            age = np.random.randint(18, 75, n_samples)
            gender = np.random.choice(['Male', 'Female'], n_samples, p=[0.45, 0.55])
            
            # 收入分布（引入双峰分布，模拟不同收入群体）
            income_low = np.random.normal(30000, 10000, int(n_samples * 0.7))
            income_high = np.random.normal(80000, 25000, int(n_samples * 0.3))
            income = np.concatenate([income_low, income_high])
            np.random.shuffle(income)
            income = np.maximum(income, 15000)  # 确保收入不低于15000
            
            # 地理信息
            region = np.random.choice(['North', 'South', 'East', 'West'], n_samples)
            city_size = np.random.choice(['Small', 'Medium', 'Large'], n_samples, p=[0.3, 0.4, 0.3])
            
            # 购买行为特征
            # 使用不同的分布生成不同类型的客户
            purchase_pattern = np.random.choice(['frequent_low_value', 'frequent_high_value', 
                                               'infrequent_low_value', 'infrequent_high_value'], 
                                               n_samples, p=[0.3, 0.15, 0.4, 0.15])
            
            purchase_frequency = np.zeros(n_samples)
            avg_purchase_value = np.zeros(n_samples)
            
            for i, pattern in enumerate(purchase_pattern):
                if pattern == 'frequent_low_value':
                    purchase_frequency[i] = np.random.uniform(10, 30)
                    avg_purchase_value[i] = np.random.uniform(50, 150)
                elif pattern == 'frequent_high_value':
                    purchase_frequency[i] = np.random.uniform(8, 25)
                    avg_purchase_value[i] = np.random.uniform(200, 500)
                elif pattern == 'infrequent_low_value':
                    purchase_frequency[i] = np.random.uniform(1, 8)
                    avg_purchase_value[i] = np.random.uniform(30, 100)
                elif pattern == 'infrequent_high_value':
                    purchase_frequency[i] = np.random.uniform(1, 6)
                    avg_purchase_value[i] = np.random.uniform(300, 1000)
            
            # 总消费和客单价
            total_spend = purchase_frequency * avg_purchase_value
            
            # 客户忠诚度特征
            membership_years = np.random.randint(0, 15, n_samples)  # 会员年限
            
            # 客户满意度和参与度
            satisfaction_score = np.random.normal(4, 0.8, n_samples)
            satisfaction_score = np.clip(satisfaction_score, 1, 5)
            
            engagement_score = np.random.normal(60, 20, n_samples)
            engagement_score = np.clip(engagement_score, 0, 100)
            
            # 线上线下渠道使用情况
            online_purchase_ratio = np.random.beta(2, 3, n_samples)  # 线上购买比例
            
            # 最近购买时间（R值）
            recency = np.random.exponential(30, n_samples)  # 最近一次购买的天数
            
            # 客户流失风险
            # 基于多个因素计算流失风险
            churn_probability = 0.5 - 0.1 * np.log10(income/1000) + 
                              0.03 * recency - 0.05 * membership_years - 
                              0.02 * satisfaction_score + 
                              np.random.normal(0, 0.1, n_samples)
            churn_probability = np.clip(churn_probability, 0.05, 0.95)
            
            # 创建DataFrame
            self.raw_data = pd.DataFrame({
                'customer_id': [f'CUST{i:04d}' for i in range(1, n_samples+1)],
                'age': age,
                'gender': gender,
                'income': income,
                'region': region,
                'city_size': city_size,
                'purchase_frequency': purchase_frequency,
                'avg_purchase_value': avg_purchase_value,
                'total_spend': total_spend,
                'membership_years': membership_years,
                'satisfaction_score': satisfaction_score,
                'engagement_score': engagement_score,
                'online_purchase_ratio': online_purchase_ratio,
                'recency': recency,
                'churn_probability': churn_probability
            })
            
            # 复制原始数据用于分析
            self.data = self.raw_data.copy()
        else:
            # 从文件加载数据
            if file_path is None:
                raise ValueError("如果不使用样本数据，必须提供文件路径")
            
            # 假设CSV文件包含必要的列
            self.raw_data = pd.read_csv(file_path)
            self.data = self.raw_data.copy()
        
        return self.data

    def data_preprocessing(self, feature_columns=None, scaling_method='standard', 
                         handle_categorical=True, engineer_features=True):
        """
        高级数据预处理
        """
        if self.data is None:
            raise ValueError("请先加载数据")
        
        df = self.data.copy()
        
        # 处理分类特征
        if handle_categorical:
            categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
            
            # 进行独热编码
            df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)
        
        # 特征工程
        if engineer_features:
            # 创建新的特征组合
            if 'income' in df.columns and 'avg_purchase_value' in df.columns:
                df['spend_to_income_ratio'] = df['avg_purchase_value'] / (df['income'] / 12)  # 支出收入比
            
            if 'purchase_frequency' in df.columns and 'membership_years' in df.columns:
                df['frequency_per_year'] = df['purchase_frequency'] / (df['membership_years'] + 1)  # 年均购买频率
            
            if 'total_spend' in df.columns and 'membership_years' in df.columns:
                df['spend_per_year'] = df['total_spend'] / (df['membership_years'] + 1)  # 年均消费
            
            # 客户价值评分（简化版）
            value_score = []
            if all(col in df.columns for col in ['total_spend', 'purchase_frequency', 'satisfaction_score']):
                for _, row in df.iterrows():
                    score = (row['total_spend'] / df['total_spend'].max()) * 0.4 +
                           (row['purchase_frequency'] / df['purchase_frequency'].max()) * 0.3 +
                           (row['satisfaction_score'] / 5) * 0.3
                    value_score.append(score)
                df['customer_value_score'] = value_score
        
        # 如果未指定特征列，使用所有数值型列（除了客户ID）
        if feature_columns is None:
            feature_columns = [col for col in df.columns 
                              if col != 'customer_id' and df[col].dtype in ['int64', 'float64']]
        
        # 选择特征
        X = df[feature_columns].copy()
        
        # 处理缺失值
        X.fillna(X.median(), inplace=True)  # 使用中位数处理缺失值，更稳健
        
        # 特征缩放
        if scaling_method == 'standard':
            self.scaler = StandardScaler()
        elif scaling_method == 'minmax':
            self.scaler = MinMaxScaler()
        elif scaling_method == 'robust':
            self.scaler = RobustScaler()
        else:
            raise ValueError("不支持的缩放方法")
        
        X_scaled = self.scaler.fit_transform(X)
        
        # 将缩放后的数据转换回DataFrame
        X_scaled_df = pd.DataFrame(X_scaled, columns=feature_columns, index=X.index)
        
        return X_scaled_df, feature_columns

    def build_autoencoder(self, input_dim, encoding_dim=10):
        """
        构建自编码器用于特征降维和提取
        """
        # 编码器
        input_layer = Input(shape=(input_dim,))
        
        # 编码层
        encoded = Dense(32, activation='relu')(input_layer)
        encoded = BatchNormalization()(encoded)
        encoded = Dropout(0.2)(encoded)
        encoded = Dense(16, activation='relu')(encoded)
        encoded = BatchNormalization()(encoded)
        encoded = Dropout(0.2)(encoded)
        encoded = Dense(encoding_dim, activation='relu')(encoded)
        
        # 解码器
        decoded = Dense(16, activation='relu')(encoded)
        decoded = BatchNormalization()(decoded)
        decoded = Dropout(0.2)(decoded)
        decoded = Dense(32, activation='relu')(decoded)
        decoded = BatchNormalization()(decoded)
        decoded = Dropout(0.2)(decoded)
        decoded = Dense(input_dim, activation='linear')(decoded)
        
        # 构建自编码器模型
        autoencoder = Model(input_layer, decoded)
        
        # 编译模型
        autoencoder.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
        
        # 构建编码器模型（用于特征提取）
        encoder = Model(input_layer, encoded)
        
        self.autoencoder = autoencoder
        
        return autoencoder, encoder

    def train_autoencoder(self, X, epochs=100, batch_size=32):
        """
        训练自编码器
        """
        if self.autoencoder is None:
            # 自动构建自编码器
            input_dim = X.shape[1]
            encoding_dim = max(2, int(input_dim / 3))  # 编码维度为输入维度的1/3，至少为2
            self.autoencoder, _ = self.build_autoencoder(input_dim, encoding_dim)
        
        # 训练自编码器
        history = self.autoencoder.fit(X, X, 
                                      epochs=epochs, 
                                      batch_size=batch_size, 
                                      validation_split=0.2, 
                                      shuffle=True, 
                                      verbose=1)
        
        # 可视化训练过程
        plt.figure(figsize=(10, 6))
        plt.plot(history.history['loss'], label='训练损失')
        plt.plot(history.history['val_loss'], label='验证损失')
        plt.title('自编码器训练过程')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        
        # 获取编码器部分
        encoder = Model(inputs=self.autoencoder.input, 
                       outputs=self.autoencoder.layers[6].output)  # 假设编码层是第7层（索引6）
        
        return encoder

    def extract_features_with_autoencoder(self, X, encoder):
        """
        使用自编码器提取特征
        """
        # 使用编码器提取特征
        X_encoded = encoder.predict(X)
        
        # 将提取的特征转换为DataFrame
        encoded_feature_columns = [f'encoded_feature_{i}' for i in range(X_encoded.shape[1])]
        X_encoded_df = pd.DataFrame(X_encoded, columns=encoded_feature_columns, index=X.index)
        
        return X_encoded_df

    def determine_optimal_clusters(self, X, max_clusters=10, methods=['kmeans']):
        """
        确定最优聚类数量（支持多种方法）
        """
        if not methods:
            methods = ['kmeans']
        
        # 为每种方法创建子图
        n_methods = len(methods)
        plt.figure(figsize=(5 * n_methods, 10))
        
        optimal_k_results = {}
        
        for i, method in enumerate(methods):
            if method == 'kmeans':
                # 肘部法则
                wcss = []  # 簇内平方和
                silhouette_scores = []
                
                for k in range(2, max_clusters + 1):
                    kmeans = KMeans(n_clusters=k, random_state=42)
                    kmeans.fit(X)
                    wcss.append(kmeans.inertia_)
                    silhouette_scores.append(silhouette_score(X, kmeans.labels_))
                
                # 可视化肘部法则
                plt.subplot(2, n_methods, i+1)
                plt.plot(range(2, max_clusters + 1), wcss, marker='o')
                plt.title('K-means - 肘部法则')
                plt.xlabel('聚类数量')
                plt.ylabel('WCSS')
                plt.grid(True)
                
                plt.subplot(2, n_methods, i+1 + n_methods)
                plt.plot(range(2, max_clusters + 1), silhouette_scores, marker='o')
                plt.title('K-means - 轮廓系数')
                plt.xlabel('聚类数量')
                plt.ylabel('轮廓系数')
                plt.grid(True)
                
                # 选择轮廓系数最大的聚类数量
                optimal_k = 2 + silhouette_scores.index(max(silhouette_scores))
                optimal_k_results['kmeans'] = optimal_k
            
            elif method == 'gmm':
                # 用于GMM的BIC和AIC
                bic_scores = []
                aic_scores = []
                
                for k in range(2, max_clusters + 1):
                    gmm = GaussianMixture(n_components=k, random_state=42)
                    gmm.fit(X)
                    bic_scores.append(gmm.bic(X))
                    aic_scores.append(gmm.aic(X))
                
                # 可视化BIC和AIC
                plt.subplot(2, n_methods, i+1)
                plt.plot(range(2, max_clusters + 1), bic_scores, marker='o', label='BIC')
                plt.plot(range(2, max_clusters + 1), aic_scores, marker='o', label='AIC')
                plt.title('GMM - BIC/AIC')
                plt.xlabel('聚类数量')
                plt.ylabel('得分')
                plt.legend()
                plt.grid(True)
                
                plt.subplot(2, n_methods, i+1 + n_methods)
                # 对于GMM，也可以计算轮廓系数
                silhouette_scores = []
                for k in range(2, max_clusters + 1):
                    gmm = GaussianMixture(n_components=k, random_state=42)
                    labels = gmm.fit_predict(X)
                    silhouette_scores.append(silhouette_score(X, labels))
                plt.plot(range(2, max_clusters + 1), silhouette_scores, marker='o')
                plt.title('GMM - 轮廓系数')
                plt.xlabel('聚类数量')
                plt.ylabel('轮廓系数')
                plt.grid(True)
                
                # 选择BIC最小的聚类数量
                optimal_k = 2 + bic_scores.index(min(bic_scores))
                optimal_k_results['gmm'] = optimal_k
        
        plt.tight_layout()
        plt.show()
        
        # 打印各方法的最优聚类数量
        print("各方法的最优聚类数量:")
        for method, k in optimal_k_results.items():
            print(f"{method}: {k}")
        
        # 返回最常出现的最优聚类数量
        if optimal_k_results:
            from collections import Counter
            most_common_k = Counter(optimal_k_results.values()).most_common(1)[0][0]
            print(f"综合最优聚类数量: {most_common_k}")
            return most_common_k
        else:
            return 4  # 默认值

    def perform_clustering(self, X, algorithm='KMeans', n_clusters=4, hyperparameter_tuning=False, **kwargs):
        """
        高级客户聚类，支持超参数调优
        """
        if algorithm == 'AutoencoderKMeans':
            # 使用自编码器+KMeans的组合方法
            print("使用自编码器+KMeans进行聚类...")
            
            # 训练自编码器
            encoder = self.train_autoencoder(X, epochs=50, batch_size=32)
            
            # 提取特征
            X_encoded = self.extract_features_with_autoencoder(X, encoder)
            
            # 在编码后的特征上执行KMeans聚类
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, **kwargs)
            self.cluster_labels = kmeans.fit_predict(X_encoded)
            
            # 保存最佳模型
            self.best_model = kmeans
            
            # 可视化编码后的特征和聚类结果
            plt.figure(figsize=(10, 8))
            # 再次降维以便可视化
            if X_encoded.shape[1] > 2:
                pca = PCA(n_components=2)
                X_visual = pca.fit_transform(X_encoded)
            else:
                X_visual = X_encoded.values
            
            scatter = plt.scatter(X_visual[:, 0], X_visual[:, 1], 
                                 c=self.cluster_labels, cmap='viridis', s=50, alpha=0.7)
            plt.title('自编码器+KMeans聚类结果可视化')
            plt.colorbar(scatter, label='聚类标签')
            plt.grid(True)
            plt.tight_layout()
            plt.show()
            
        else:
            if algorithm not in self.models:
                raise ValueError(f"不支持的聚类算法: {algorithm}")
            
            # 超参数调优
            if hyperparameter_tuning:
                print(f"对{algorithm}进行超参数调优...")
                
                if algorithm == 'KMeans':
                    param_grid = {
                        'n_clusters': range(2, 8),
                        'init': ['k-means++', 'random'],
                        'max_iter': [100, 200, 300]
                    }
                    grid_search = GridSearchCV(estimator=KMeans(random_state=42),
                                             param_grid=param_grid,
                                             scoring='silhouette_score',
                                             cv=3,  # 对于聚类，交叉验证的意义有限，但仍然可以使用
                                             n_jobs=-1, verbose=1)
                    grid_search.fit(X)
                    
                    print(f"最佳参数: {grid_search.best_params_}")
                    model = grid_search.best_estimator_
                    
                elif algorithm == 'GaussianMixture':
                    param_grid = {
                        'n_components': range(2, 8),
                        'covariance_type': ['full', 'tied', 'diag', 'spherical'],
                        'reg_covar': [1e-6, 1e-5, 1e-4]
                    }
                    grid_search = GridSearchCV(estimator=GaussianMixture(random_state=42),
                                             param_grid=param_grid,
                                             scoring='silhouette_score',
                                             cv=3, n_jobs=-1, verbose=1)
                    grid_search.fit(X)
                    
                    print(f"最佳参数: {grid_search.best_params_}")
                    model = grid_search.best_estimator_
                    
                else:
                    # 对于其他算法，使用默认参数
                    print(f"{algorithm}暂不支持超参数调优，使用默认参数")
                    if algorithm == 'KMeans':
                        model = KMeans(n_clusters=n_clusters, random_state=42, **kwargs)
                    elif algorithm == 'Hierarchical':
                        model = AgglomerativeClustering(n_clusters=n_clusters, **kwargs)
                    elif algorithm == 'DBSCAN':
                        model = DBSCAN(**kwargs)
                    elif algorithm == 'GaussianMixture':
                        model = GaussianMixture(n_components=n_clusters, random_state=42, **kwargs)
            else:
                # 根据算法设置参数
                if algorithm == 'KMeans':
                    model = KMeans(n_clusters=n_clusters, random_state=42, **kwargs)
                elif algorithm == 'Hierarchical':
                    model = AgglomerativeClustering(n_clusters=n_clusters, **kwargs)
                elif algorithm == 'DBSCAN':
                    model = DBSCAN(**kwargs)
                elif algorithm == 'GaussianMixture':
                    model = GaussianMixture(n_components=n_clusters, random_state=42, **kwargs)
            
            # 执行聚类
            self.cluster_labels = model.fit_predict(X)
            
            # 保存最佳模型
            self.best_model = model
        
        print(f"使用{algorithm}算法完成客户聚类")
        
        # 统计每个簇的客户数量
        unique_labels, counts = np.unique(self.cluster_labels, return_counts=True)
        print("各簇客户数量:")
        for label, count in zip(unique_labels, counts):
            print(f"簇 {label}: {count} 个客户 ({count/len(X)*100:.2f}%)")
        
        return self.cluster_labels

    def calculate_customer_lifetime_value(self, frequency_col='purchase_frequency', 
                                        recency_col='recency', 
                                        monetary_col='avg_purchase_value', 
                                        age_col='membership_years'):
        """
        计算客户生命周期价值(CLV)
        """
        if self.data is None:
            raise ValueError("请先加载数据")
        
        df = self.data.copy()
        
        # 确保所有需要的列都存在
        required_cols = [frequency_col, recency_col, monetary_col, age_col]
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"数据中缺少必要的列: {col}")
        
        # 准备用于lifetimes库的数据
        # 注意：lifetimes库假设recency是最近一次购买距离第一次购买的时间，这里我们简化处理
        clv_data = df[[frequency_col, recency_col, monetary_col, age_col]].copy()
        
        # 重命名列以符合lifetimes库的要求
        clv_data.columns = ['frequency', 'recency', 'monetary_value', 'T']
        
        # 过滤掉频率为0的客户（非活跃客户）
        clv_data = clv_data[clv_data['frequency'] > 0].copy()
        
        # 确保所有值都是正数
        clv_data = clv_data[(clv_data['frequency'] > 0) &
                           (clv_data['recency'] > 0) &
                           (clv_data['monetary_value'] > 0)]
        
        # 拟合BG/NBD模型（用于预测客户活跃度）
        bgf = BetaGeoFitter(penalizer_coef=0.01)
        bgf.fit(clv_data['frequency'], clv_data['recency'], clv_data['T'])
        
        # 拟合Gamma-Gamma模型（用于预测客户消费金额）
        ggf = GammaGammaFitter(penalizer_coef=0.01)
        ggf.fit(clv_data['frequency'], clv_data['monetary_value'])
        
        # 预测客户生命周期价值
        # 这里预测未来12个月的CLV
        clv = ggf.customer_lifetime_value(
            bgf,
            clv_data['frequency'],
            clv_data['recency'],
            clv_data['T'],
            clv_data['monetary_value'],
            time=12,  # 预测未来12个月
            discount_rate=0.01  # 月折现率
        )
        
        # 将CLV结果合并回原始数据
        clv_result = pd.DataFrame({
            'customer_id': df.loc[clv_data.index, 'customer_id'],
            'clv': clv
        })
        
        # 对于没有足够数据计算CLV的客户，使用平均值
        all_clv = pd.DataFrame({'customer_id': df['customer_id']})
        all_clv = all_clv.merge(clv_result, on='customer_id', how='left')
        all_clv['clv'].fillna(all_clv['clv'].mean(), inplace=True)
        
        # 将CLV添加到数据中
        df = df.merge(all_clv, on='customer_id')
        self.data = df
        
        # 保存CLV结果
        self.customer_lifetime_value = all_clv
        
        # 可视化CLV相关图表
        plt.figure(figsize=(15, 10))
        
        # 1. 频率-最近购买时间矩阵
        plt.subplot(2, 2, 1)
        plot_frequency_recency_matrix(bgf)
        plt.title('客户活跃度矩阵')
        
        # 2. 客户存活概率矩阵
        plt.subplot(2, 2, 2)
        plot_probability_alive_matrix(bgf)
        plt.title('客户存活概率矩阵')
        
        # 3. CLV分布
        plt.subplot(2, 2, 3)
        sns.histplot(all_clv['clv'], bins=30, kde=True)
        plt.title('客户生命周期价值分布')
        plt.xlabel('CLV')
        plt.ylabel('频数')
        
        # 4. CLV与客户特征的关系
        if 'total_spend' in df.columns:
            plt.subplot(2, 2, 4)
            sns.scatterplot(x=df['total_spend'], y=df['clv'])
            plt.title('CLV与总消费的关系')
            plt.xlabel('总消费')
            plt.ylabel('CLV')
        
        plt.tight_layout()
        plt.show()
        
        print(f"客户生命周期价值计算完成，平均CLV: {all_clv['clv'].mean():.2f}")
        
        return all_clv

    def evaluate_clustering(self, X):
        """
        高级聚类评估
        """
        if self.cluster_labels is None:
            raise ValueError("请先执行聚类")
        
        # 计算评估指标
        n_clusters = len(np.unique(self.cluster_labels))
        
        # 只有当聚类数量大于1且小于样本数量时才能计算这些指标
        if n_clusters > 1 and n_clusters < len(X):
            try:
                silhouette_avg = silhouette_score(X, self.cluster_labels)
                db_score = davies_bouldin_score(X, self.cluster_labels)
                ch_score = calinski_harabasz_score(X, self.cluster_labels)
                
                self.metrics = {
                    'Silhouette Score': silhouette_avg,
                    'Davies-Bouldin Score': db_score,
                    'Calinski-Harabasz Score': ch_score,
                    'Number of Clusters': n_clusters
                }
                
                print("聚类评估指标:")
                print(f"轮廓系数: {silhouette_avg:.4f} (越接近1越好)")
                print(f"Davies-Bouldin指数: {db_score:.4f} (值越小越好)")
                print(f"Calinski-Harabasz指数: {ch_score:.4f} (值越大越好)")
            except Exception as e:
                print(f"评估聚类结果时出错: {e}")
        else:
            print("聚类数量不合适，无法计算评估指标")
        
        return self.metrics

    def visualize_clusters(self, X, feature_columns, method='pca'):
        """
        高级聚类可视化
        """
        if self.cluster_labels is None:
            raise ValueError("请先执行聚类")
        
        # 降维以便可视化
        if X.shape[1] > 2:
            if method == 'pca':
                reducer = PCA(n_components=2)
            elif method == 'tsne':
                reducer = TSNE(n_components=2, random_state=42, perplexity=30)
            elif method == 'umap':
                reducer = UMAP(n_components=2, random_state=42)
            elif method == 'kpca':
                reducer = KernelPCA(n_components=2, kernel='rbf', random_state=42)
            elif method == 'ica':
                reducer = FastICA(n_components=2, random_state=42)
            else:
                raise ValueError("不支持的降维方法")
            
            X_reduced = reducer.fit_transform(X)
            if hasattr(reducer, 'explained_variance_ratio_'):
                print(f"{method.upper()}降维保留的方差比例: {sum(reducer.explained_variance_ratio_):.4f}")
        else:
            # 如果特征数量小于等于2，直接使用前两个特征
            X_reduced = X.iloc[:, :2].values
        
        # 可视化聚类结果
        plt.figure(figsize=(10, 8))
        scatter = plt.scatter(X_reduced[:, 0], X_reduced[:, 1], 
                             c=self.cluster_labels, cmap='viridis', s=50, alpha=0.7)
        plt.title(f'客户聚类结果可视化 ({method.upper()}降维)')
        plt.xlabel('特征1')
        plt.ylabel('特征2')
        plt.colorbar(scatter, label='聚类标签')
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        
        # 对于层次聚类，绘制树状图
        if isinstance(self.best_model, AgglomerativeClustering):
            plt.figure(figsize=(12, 8))
            Z = linkage(X, 'ward')
            dendrogram(Z, truncate_mode='lastp', p=10, leaf_rotation=45., leaf_font_size=15.)
            plt.title('层次聚类树状图')
            plt.xlabel('样本')
            plt.ylabel('距离')
            plt.tight_layout()
            plt.show()

    def analyze_cluster_profiles(self, feature_columns):
        """
        高级簇概况分析
        """
        if self.cluster_labels is None:
            raise ValueError("请先执行聚类")
        
        # 将聚类标签添加到原始数据中
        result_data = self.raw_data.copy()
        result_data['cluster'] = self.cluster_labels
        
        # 如果计算了CLV，也添加到数据中
        if self.customer_lifetime_value is not None:
            result_data = result_data.merge(self.customer_lifetime_value, on='customer_id', how='left')
            if 'clv' not in feature_columns:
                feature_columns.append('clv')
        
        # 计算每个簇的特征统计量
        cluster_stats = {}
        for cluster in np.unique(self.cluster_labels):
            cluster_data = result_data[result_data['cluster'] == cluster]
            cluster_stats[cluster] = {
                'count': len(cluster_data),
                'percentage': len(cluster_data) / len(result_data) * 100
            }
            
            # 对每个数值型特征计算统计量
            for feature in feature_columns:
                if feature in cluster_data.columns and pd.api.types.is_numeric_dtype(cluster_data[feature]):
                    cluster_stats[cluster][f'{feature}_mean'] = cluster_data[feature].mean()
                    cluster_stats[cluster][f'{feature}_median'] = cluster_data[feature].median()
                    cluster_stats[cluster][f'{feature}_std'] = cluster_data[feature].std()
        
        # 转换为DataFrame以便查看
        cluster_profiles = pd.DataFrame(cluster_stats).T
        
        print("\n各簇详细特征统计:")
        print(cluster_profiles)
        
        # 可视化每个簇的关键特征雷达图
        # 选择一些关键特征进行雷达图展示
        key_features = []
        for feature in feature_columns:
            if len(key_features) < 5 and feature in result_data.columns and pd.api.types.is_numeric_dtype(result_data[feature]):
                key_features.append(feature)
        
        if key_features:
            # 数据归一化以便在雷达图上比较
            normalized_data = {}
            for cluster in np.unique(self.cluster_labels):
                cluster_data = result_data[result_data['cluster'] == cluster]
                normalized_row = {}
                for feature in key_features:
                    # 归一化到0-1范围
                    min_val = result_data[feature].min()
                    max_val = result_data[feature].max()
                    if max_val > min_val:
                        normalized_row[feature] = (cluster_data[feature].mean() - min_val) / (max_val - min_val)
                    else:
                        normalized_row[feature] = 0.5  # 如果所有值都相同，设置为中间值
                normalized_data[cluster] = normalized_row
            
            # 创建雷达图
            plt.figure(figsize=(10, 10))
            
            # 计算角度
            angles = np.linspace(0, 2 * np.pi, len(key_features), endpoint=False).tolist()
            # 闭合雷达图
            key_features_closed = key_features + [key_features[0]]
            angles_closed = angles + [angles[0]]
            
            # 绘制每个簇的数据
            for cluster in np.unique(self.cluster_labels):
                values = [normalized_data[cluster][feature] for feature in key_features]
                values_closed = values + [values[0]]
                plt.polar(angles_closed, values_closed, 'o-', linewidth=2, label=f'簇 {cluster}')
                plt.fill(angles_closed, values_closed, alpha=0.1)
            
            # 设置雷达图的标签和标题
            plt.thetagrids(np.degrees(angles), key_features_closed[:-1])
            plt.title('各簇关键特征雷达图 (归一化)')
            plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
            plt.grid(True)
            plt.tight_layout()
            plt.show()
        
        # 热力图展示各簇特征对比（使用均值）
        mean_profiles = pd.DataFrame()
        for cluster in np.unique(self.cluster_labels):
            cluster_data = result_data[result_data['cluster'] == cluster]
            mean_series = cluster_data[feature_columns].mean()
            mean_profiles[f'簇 {cluster}'] = mean_series
        
        plt.figure(figsize=(12, 8))
        sns.heatmap(mean_profiles.T, annot=True, cmap='YlGnBu')
        plt.title('各簇特征均值对比')
        plt.tight_layout()
        plt.show()
        
        return cluster_profiles

    def generate_segmentation_report(self, feature_columns):
        """
        生成高级客户细分报告
        """
        if self.cluster_labels is None:
            raise ValueError("请先执行聚类")
        
        # 分析簇概况
        cluster_profiles = self.analyze_cluster_profiles(feature_columns)
        
        # 将聚类标签添加到原始数据中
        result_data = self.raw_data.copy()
        result_data['cluster'] = self.cluster_labels
        
        # 如果计算了CLV，也添加到数据中
        if self.customer_lifetime_value is not None:
            result_data = result_data.merge(self.customer_lifetime_value, on='customer_id', how='left')
        
        # 为每个簇生成详细的描述性标签和特征
        segment_details = {}
        n_clusters = len(np.unique(self.cluster_labels))
        
        for cluster in np.unique(self.cluster_labels):
            cluster_data = result_data[result_data['cluster'] == cluster]
            cluster_size = len(cluster_data)
            cluster_percentage = cluster_size / len(result_data) * 100
            
            # 基于多个关键特征生成簇描述
            descriptors = []
            
            # 基于消费能力
            if 'total_spend' in cluster_data.columns:
                spend_percentile = np.percentile(result_data['total_spend'], [25, 50, 75])
                cluster_spend = cluster_data['total_spend'].mean()
                if cluster_spend >= spend_percentile[2]:
                    descriptors.append('高消费')
                elif cluster_spend >= spend_percentile[1]:
                    descriptors.append('中等消费')
                else:
                    descriptors.append('低消费')
            
            # 基于购买频率
            if 'purchase_frequency' in cluster_data.columns:
                freq_percentile = np.percentile(result_data['purchase_frequency'], [25, 50, 75])
                cluster_freq = cluster_data['purchase_frequency'].mean()
                if cluster_freq >= freq_percentile[2]:
                    descriptors.append('高频购买')
                elif cluster_freq >= freq_percentile[1]:
                    descriptors.append('中频购买')
                else:
                    descriptors.append('低频购买')
            
            # 基于客户价值
            if 'clv' in cluster_data.columns:
                clv_percentile = np.percentile(result_data['clv'].dropna(), [25, 50, 75])
                cluster_clv = cluster_data['clv'].mean()
                if cluster_clv >= clv_percentile[2]:
                    descriptors.append('高价值')
                elif cluster_clv >= clv_percentile[1]:
                    descriptors.append('中等价值')
                else:
                    descriptors.append('低价值')
            
            # 基于客户忠诚度
            if 'membership_years' in cluster_data.columns:
                loyalty_percentile = np.percentile(result_data['membership_years'], [25, 50, 75])
                cluster_loyalty = cluster_data['membership_years'].mean()
                if cluster_loyalty >= loyalty_percentile[2]:
                    descriptors.append('高忠诚度')
                elif cluster_loyalty >= loyalty_percentile[1]:
                    descriptors.append('中等忠诚度')
                else:
                    descriptors.append('低忠诚度')
            
            # 基于满意度
            if 'satisfaction_score' in cluster_data.columns:
                satisfaction_threshold = 4.0  # 假设4分以上为高满意度
                cluster_satisfaction = cluster_data['satisfaction_score'].mean()
                if cluster_satisfaction >= satisfaction_threshold:
                    descriptors.append('高满意度')
                else:
                    descriptors.append('一般满意度')
            
            # 生成段标签
            if descriptors:
                segment_label = '-'.join(descriptors)
            else:
                segment_label = f'客户群体{cluster+1}'
            
            # 收集关键特征统计
            key_stats = {}
            for feature in feature_columns:
                if feature in cluster_data.columns and pd.api.types.is_numeric_dtype(cluster_data[feature]):
                    key_stats[feature] = {
                        'mean': cluster_data[feature].mean(),
                        'median': cluster_data[feature].median(),
                        'std': cluster_data[feature].std()
                    }
            
            # 收集营销策略建议
            marketing_recommendations = []
            if '高价值' in segment_label or '高消费' in segment_label:
                marketing_recommendations.append('提供VIP服务和专属优惠')
                marketing_recommendations.append('定期进行个性化沟通和关怀')
            
            if '低消费' in segment_label or '低价值' in segment_label:
                marketing_recommendations.append('提供入门级产品和促销活动')
                marketing_recommendations.append('通过交叉销售和向上销售提升价值')
            
            if '高频购买' in segment_label:
                marketing_recommendations.append('建立会员积分和奖励机制')
                marketing_recommendations.append('提供订阅服务和定期配送选项')
            
            if '低频购买' in segment_label:
                marketing_recommendations.append('定期发送提醒和个性化推荐')
                marketing_recommendations.append('分析购买障碍并提供解决方案')
            
            if '高忠诚度' in segment_label:
                marketing_recommendations.append('邀请参与产品测试和反馈')
                marketing_recommendations.append('建立品牌大使计划')
            
            if '低忠诚度' in segment_label:
                marketing_recommendations.append('分析流失原因并改进客户体验')
                marketing_recommendations.append('提供忠诚度奖励计划')
            
            # 存储段详细信息
            segment_details[cluster] = {
                'label': segment_label,
                'size': cluster_size,
                'percentage': cluster_percentage,
                'key_stats': key_stats,
                'marketing_recommendations': marketing_recommendations
            }
        
        # 打印详细的客户细分报告
        print("\n===== 高级客户细分报告 =====")
        for cluster in sorted(segment_details.keys()):
            details = segment_details[cluster]
            print(f"\n客户群体: {details['label']} (簇 {cluster})")
            print(f"  客户数量: {details['size']} ({details['percentage']:.2f}%)")
            print("  关键特征统计:")
            for feature, stats in details['key_stats'].items():
                print(f"    {feature}: 均值={stats['mean']:.2f}, 中位数={stats['median']:.2f}, 标准差={stats['std']:.2f}")
            print("  营销策略建议:")
            for recommendation in details['marketing_recommendations']:
                print(f"    - {recommendation}")
        print("====================")
        
        return {
            'segment_details': segment_details,
            'cluster_profiles': cluster_profiles
        }

    def dynamic_segmentation(self, X_static, X_dynamic, time_window=30, min_cluster_size=10):
        """
        实现动态客户细分，考虑客户行为的变化
        """
        if self.cluster_labels is None:
            raise ValueError("请先执行初始聚类")
        
        # 这里我们简化实现，实际应用中可能需要更复杂的时序分析
        # X_static: 静态特征（如人口统计信息）
        # X_dynamic: 动态特征（如最近一段时间的购买行为）
        
        # 结合静态和动态特征
        X_combined = pd.concat([X_static, X_dynamic], axis=1)
        
        # 在组合特征上执行聚类
        # 为了保持一定的稳定性，我们要求每个簇至少有min_cluster_size个客户
        n_clusters = max(2, len(np.unique(self.cluster_labels)))
        
        # 使用调整后的DBSCAN算法，它对密度变化的数据更友好
        from sklearn.cluster import OPTICS
        
        try:
            # 使用OPTICS算法
            optics = OPTICS(min_samples=min_cluster_size, xi=0.05, min_cluster_size=0.05)
            dynamic_labels = optics.fit_predict(X_combined)
            
            # 统计每个簇的客户数量
            unique_labels, counts = np.unique(dynamic_labels, return_counts=True)
            print("\n动态细分结果:")
            for label, count in zip(unique_labels, counts):
                if label == -1:
                    print(f"离群点: {count} 个客户 ({count/len(X_combined)*100:.2f}%)")
                else:
                    print(f"动态簇 {label}: {count} 个客户 ({count/len(X_combined)*100:.2f}%)")
            
            # 可视化动态细分结果
            if X_combined.shape[1] > 2:
                pca = PCA(n_components=2)
                X_reduced = pca.fit_transform(X_combined)
            else:
                X_reduced = X_combined.values
            
            plt.figure(figsize=(10, 8))
            scatter = plt.scatter(X_reduced[:, 0], X_reduced[:, 1], 
                                 c=dynamic_labels, cmap='plasma', s=50, alpha=0.7)
            plt.title('动态客户细分结果')
            plt.colorbar(scatter, label='动态簇标签')
            plt.grid(True)
            plt.tight_layout()
            plt.show()
            
            return dynamic_labels
        except Exception as e:
            print(f"执行动态细分时出错: {e}")
            print("回退到K-means算法")
            
            # 如果OPTICS失败，回退到K-means
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            dynamic_labels = kmeans.fit_predict(X_combined)
            
            return dynamic_labels

    def export_segmentation_results(self, output_format='csv', output_path='customer_segmentation_results'):
        """
        导出客户细分结果
        """
        if self.cluster_labels is None:
            raise ValueError("请先执行聚类")
        
        # 准备结果数据
        result_data = self.raw_data.copy()
        result_data['cluster'] = self.cluster_labels
        
        # 如果计算了CLV，也添加到结果中
        if self.customer_lifetime_value is not None:
            result_data = result_data.merge(self.customer_lifetime_value, on='customer_id', how='left')
        
        # 导出结果
        if output_format == 'csv':
            output_file = f"{output_path}.csv"
            result_data.to_csv(output_file, index=False)
            print(f"客户细分结果已导出到CSV文件: {output_file}")
        elif output_format == 'excel':
            try:
                import openpyxl
                output_file = f"{output_path}.xlsx"
                result_data.to_excel(output_file, index=False)
                print(f"客户细分结果已导出到Excel文件: {output_file}")
            except ImportError:
                print("未找到openpyxl库，请安装后重试")
                print("尝试导出为CSV文件...")
                output_file = f"{output_path}.csv"
                result_data.to_csv(output_file, index=False)
                print(f"客户细分结果已导出到CSV文件: {output_file}")
        elif output_format == 'json':
            output_file = f"{output_path}.json"
            result_data.to_json(output_file, orient='records', force_ascii=False, indent=2)
            print(f"客户细分结果已导出到JSON文件: {output_file}")
        else:
            raise ValueError("不支持的输出格式")
        
        return output_file

# 使用示例
if __name__ == "__main__":
    # 创建高级AI客户细分器实例
    advanced_segmenter = AdvancedAICustomerSegmentation()
    
    print("正在初始化高级AI客户细分系统...")
    
    # 加载样本数据
    print("\n加载高级样本客户数据...")
    advanced_segmenter.load_data(sample_data=True, n_samples=1000)
    print(f"数据加载完成，共有{len(advanced_segmenter.data)}个客户记录")
    
    # 数据预处理（包含特征工程）
    print("\n预处理客户数据并执行特征工程...")
    feature_columns = ['age', 'income', 'purchase_frequency', 'avg_purchase_value', 
                      'total_spend', 'membership_years', 'satisfaction_score', 
                      'engagement_score', 'online_purchase_ratio', 'recency', 'churn_probability']
    X_scaled, selected_features = advanced_segmenter.data_preprocessing(
        feature_columns, 
        scaling_method='robust',
        handle_categorical=True,
        engineer_features=True
    )
    print(f"预处理完成，使用的特征: {selected_features}")
    
    # 计算客户生命周期价值
    print("\n计算客户生命周期价值(CLV)...")
    clv_results = advanced_segmenter.calculate_customer_lifetime_value()
    
    # 重新预处理数据（包含CLV）
    print("\n重新预处理数据（包含CLV）...")
    new_feature_columns = selected_features + ['clv'] if 'clv' in advanced_segmenter.data.columns else selected_features
    X_scaled_with_clv, final_features = advanced_segmenter.data_preprocessing(new_feature_columns)
    
    # 确定最优聚类数量（使用多种方法）
    print("\n使用多种方法确定最优聚类数量...")
    optimal_k = advanced_segmenter.determine_optimal_clusters(X_scaled_with_clv, max_clusters=8, methods=['kmeans', 'gmm'])
    
    # 执行高级客户聚类（包含超参数调优）
    print("\n执行高级客户聚类...")
    # 可以尝试不同的算法：'KMeans', 'GaussianMixture', 'Hierarchical', 'DBSCAN', 'AutoencoderKMeans'
    cluster_labels = advanced_segmenter.perform_clustering(
        X_scaled_with_clv, 
        algorithm='KMeans', 
        n_clusters=optimal_k, 
        hyperparameter_tuning=True
    )
    
    # 评估聚类结果
    print("\n评估聚类结果...")
    metrics = advanced_segmenter.evaluate_clustering(X_scaled_with_clv)
    
    # 可视化聚类结果（使用不同的降维方法）
    print("\n使用UMAP可视化聚类结果...")
    advanced_segmenter.visualize_clusters(X_scaled_with_clv, final_features, method='umap')
    
    # 分析簇概况
    print("\n分析各簇详细特征概况...")
    cluster_profiles = advanced_segmenter.analyze_cluster_profiles(final_features)
    
    # 生成高级客户细分报告
    print("\n生成高级客户细分报告...")
    report = advanced_segmenter.generate_segmentation_report(final_features)
    
    # 执行动态细分（如果有动态数据）
    print("\n执行动态客户细分模拟...")
    # 这里我们使用部分特征作为动态特征进行模拟
    dynamic_features = ['purchase_frequency', 'avg_purchase_value', 'recency', 'churn_probability']
    X_dynamic = X_scaled_with_clv[dynamic_features].copy()
    X_static = X_scaled_with_clv.drop(columns=dynamic_features)
    dynamic_labels = advanced_segmenter.dynamic_segmentation(X_static, X_dynamic)
    
    # 导出细分结果
    print("\n导出客户细分结果...")
    output_file = advanced_segmenter.export_segmentation_results(output_format='csv')
    
    print("\n高级AI客户细分系统运行完成！")

## 最佳实践

### 1. 工具选择
选择适合的AI客户细分工具时，应考虑以下因素：

- **数据规模**：对于大规模数据集，K-means和DBSCAN通常比层次聚类更高效
- **数据类型**：混合类型数据可能需要特殊处理或选择支持混合数据的聚类算法
- **业务需求**：如果需要解释聚类结果，应选择较容易解释的算法如K-means；如果关注异常检测，可以考虑DBSCAN
- **计算资源**：深度学习方法（如自编码器）通常需要更多的计算资源

常用的AI客户细分工具包括：
- **开源库**：scikit-learn、TensorFlow、PyTorch、Lifetimes
- **商业软件**：SAS Customer Intelligence 360、Adobe Analytics、IBM Customer Experience Analytics
- **专业平台**：Alation、KNIME、 RapidMiner

### 2. 有效使用策略

- **数据质量优先**：确保数据的准确性、完整性和时效性是成功进行客户细分的基础
- **多维度分析**：结合人口统计、行为、交易和态度等多维度数据进行细分
- **动态更新**：定期更新客户细分模型，以适应客户行为的变化
- **结合业务知识**：在算法结果的基础上，结合业务专家的知识进行最终的客户群体定义
- **小规模测试**：在全量应用前，先在小范围内测试细分结果和相应的营销策略
- **持续优化**：根据细分结果的应用效果，不断优化细分模型和特征选择

### 3. 常见误区

- **过度细分**：创建过多的客户群体可能导致资源分散，难以制定有效的营销策略
- **忽视客户变化**：客户的需求和行为会随时间变化，静态的细分模型可能很快过时
- **过分依赖算法**：纯粹依靠算法结果而忽略业务知识和直觉可能导致不实用的细分方案
- **数据偏见**：如果训练数据存在偏见，细分结果可能也会带有偏见，导致不公平的营销决策
- **忽视可操作性**：细分结果应该能够指导具体的营销策略和行动，否则就失去了意义
- **忽略成本效益**：客户细分应该带来明确的商业价值，否则可能不值得投入相应的资源

### 4. 伦理与法律问题

- **数据隐私**：确保客户数据的收集、存储和使用符合相关的隐私法规（如GDPR、CCPA等）
- **算法公平性**：避免基于敏感属性（如种族、性别、年龄等）的歧视性细分
- **透明度**：向客户解释数据使用方式和细分目的，提高算法决策的透明度
- **数据安全**：采取适当的安全措施，防止客户数据泄露
- **同意机制**：确保在收集和使用客户数据前获得适当的同意
- **责任归属**：明确AI决策的责任归属，建立有效的监督和审核机制

通过遵循这些最佳实践，企业可以更有效地利用AI客户细分技术，提高营销效率，提升客户体验，增强竞争力。