# AI销售预测

## 基本原理
AI销售预测是利用人工智能技术对未来一段时间内的销售情况进行预测的过程。它通过分析历史销售数据、市场趋势、季节性因素、经济指标等多种数据源，建立预测模型，帮助企业制定合理的销售计划、生产计划和库存管理策略。

### 技术方法
AI销售预测常用的技术方法包括：
1. **时间序列分析**：如ARIMA、SARIMA、Prophet等模型
2. **机器学习算法**：如随机森林、梯度提升树、支持向量机等
3. **深度学习模型**：如LSTM、GRU、Transformer等
4. **混合模型**：结合多种算法的优势
5. **迁移学习**：将其他领域的知识应用到销售预测中

### 核心原理
AI销售预测的核心原理包括：
1. **数据驱动决策**：基于历史数据中的模式进行预测
2. **特征工程**：提取影响销售的关键特征
3. **模型选择与优化**：选择最适合特定业务场景的预测模型
4. **误差评估与改进**：通过评估预测误差持续优化模型
5. **不确定性量化**：提供预测结果的置信区间

### 常用模型
- **ARIMA/SARIMA**：适合具有季节性和趋势性的时间序列数据
- **Facebook Prophet**：适合处理节假日和异常事件影响的预测
- **随机森林/梯度提升树**：适合处理多变量影响的复杂销售场景
- **LSTM/GRU**：适合捕捉长期依赖关系的时间序列预测
- **XGBoost/LightGBM**：适合处理大规模数据和复杂特征的预测

## 应用场景
AI销售预测在企业中有广泛的应用场景：

### 1. 短期销售预测
预测未来1-3个月的销售情况，帮助企业制定短期销售目标和资源分配计划。

### 2. 中期销售预测
预测未来3-12个月的销售情况，支持生产计划、库存管理和供应链优化。

### 3. 长期销售预测
预测未来1-3年的销售趋势，为企业战略规划、投资决策和市场扩张提供依据。

### 4. 产品生命周期管理
预测新产品的销售曲线和现有产品的生命周期阶段，帮助企业制定产品策略。

### 5. 区域销售预测
预测不同地区的销售情况，优化区域资源配置和市场策略。

### 6. 渠道销售预测
预测不同销售渠道的销售表现，优化渠道策略和资源分配。

### 7. 促销效果预测
预测促销活动对销售的影响，优化促销策略和预算分配。

### 8. 库存需求预测
基于销售预测制定库存计划，减少库存积压和缺货风险。

## 基础示例：使用Python实现AI销售预测
下面是一个使用Python实现的基础AI销售预测系统示例，包含数据加载、预处理、模型训练和预测功能。

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from statsmodels.tsa.seasonal import seasonal_decompose
import warnings
warnings.filterwarnings('ignore')

class AISalesForecaster:
    """
    基础AI销售预测系统
    """
    def __init__(self):
        """
        初始化销售预测器
        """
        self.model = None
        self.data = None
        self.features = None
        self.target = None
        self.metrics = {}
        
    def load_data(self, file_path=None, sample_data=True, n_samples=365):
        """
        加载销售数据
        """
        if sample_data:
            # 生成样本销售数据
            dates = pd.date_range(start='2022-01-01', periods=n_samples, freq='D')
            
            # 生成基础销售数据（带趋势和季节性）
            base_sales = 100 + 0.5 * np.arange(n_samples)  # 基础趋势
            seasonal = 30 * np.sin(2 * np.pi * np.arange(n_samples) / 7)  # 周季节性
            seasonal += 50 * np.sin(2 * np.pi * np.arange(n_samples) / 30)  # 月季节性
            random_noise = np.random.normal(0, 10, n_samples)  # 随机噪声
            
            # 添加一些随机事件（如促销）
            promotions = np.zeros(n_samples)
            promotion_days = np.random.choice(n_samples, size=int(n_samples * 0.1), replace=False)
            promotions[promotion_days] = 50 + np.random.normal(0, 20, len(promotion_days))
            
            # 总销售额
            sales = base_sales + seasonal + random_noise + promotions
            sales = np.maximum(sales, 0)  # 确保销售额非负
            
            # 创建DataFrame
            self.data = pd.DataFrame({
                'date': dates,
                'sales': sales,
                'promotion': promotions > 0
            })
            
            # 添加一些额外特征
            self.data['day_of_week'] = self.data['date'].dt.dayofweek
            self.data['is_weekend'] = self.data['day_of_week'].isin([5, 6])
            self.data['month'] = self.data['date'].dt.month
            self.data['quarter'] = self.data['date'].dt.quarter
        else:
            # 从文件加载数据
            if file_path is None:
                raise ValueError("如果不使用样本数据，必须提供文件路径")
            
            # 假设CSV文件包含'date'和'sales'列
            self.data = pd.read_csv(file_path)
            self.data['date'] = pd.to_datetime(self.data['date'])
            
        # 设置日期为索引
        self.data.set_index('date', inplace=True)
        
        return self.data
    
    def explore_data(self):
        """
        探索数据
        """
        if self.data is None:
            raise ValueError("请先加载数据")
        
        print("数据概览：")
        print(self.data.head())
        print("\n数据统计信息：")
        print(self.data.describe())
        
        # 可视化销售数据
        plt.figure(figsize=(12, 6))
        plt.plot(self.data['sales'])
        plt.title('销售时间序列')
        plt.xlabel('日期')
        plt.ylabel('销售额')
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        
        # 季节性分解
        try:
            result = seasonal_decompose(self.data['sales'], model='additive', period=7)  # 假设周季节性
            fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(12, 8))
            result.observed.plot(ax=ax1)
            ax1.set_title('原始数据')
            result.trend.plot(ax=ax2)
            ax2.set_title('趋势')
            result.seasonal.plot(ax=ax3)
            ax3.set_title('季节性')
            result.resid.plot(ax=ax4)
            ax4.set_title('残差')
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"季节性分解失败：{e}")
    
    def preprocess_data(self, target_column='sales', feature_columns=None, forecast_horizon=7):
        """
        预处理数据
        """
        if self.data is None:
            raise ValueError("请先加载数据")
        
        # 设置目标变量
        self.target = target_column
        
        # 创建滞后特征
        df = self.data.copy()
        
        # 如果未指定特征列，使用所有列（除了目标列）
        if feature_columns is None:
            feature_columns = [col for col in df.columns if col != target_column]
        
        # 添加滞后特征
        for i in range(1, 8):  # 添加过去7天的销售数据作为特征
            df[f'sales_lag_{i}'] = df[target_column].shift(i)
            feature_columns.append(f'sales_lag_{i}')
        
        # 添加移动平均特征
        df['sales_ma_7'] = df[target_column].rolling(window=7).mean()
        df['sales_ma_30'] = df[target_column].rolling(window=30).mean()
        feature_columns.extend(['sales_ma_7', 'sales_ma_30'])
        
        # 删除包含NaN的行
        df.dropna(inplace=True)
        
        # 准备特征和目标
        self.features = feature_columns
        X = df[self.features]
        y = df[target_column]
        
        # 划分训练集和测试集
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
        
        return X_train, X_test, y_train, y_test
    
    def train_model(self, X_train, y_train):
        """
        训练预测模型
        """
        # 使用随机森林回归器
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        
        print("模型训练完成")
        
        # 特征重要性分析
        importances = self.model.feature_importances_
        indices = np.argsort(importances)[::-1]
        
        print("\n特征重要性：")
        for f in range(min(10, len(X_train.columns))):  # 显示前10个重要特征
            print(f"{f+1}. {X_train.columns[indices[f]]}: {importances[indices[f]]:.4f}")
        
        return self.model
    
    def evaluate_model(self, X_test, y_test):
        """
        评估模型性能
        """
        if self.model is None:
            raise ValueError("请先训练模型")
        
        # 进行预测
        y_pred = self.model.predict(X_test)
        
        # 计算评估指标
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)
        
        # 保存评估指标
        self.metrics = {
            'MAE': mae,
            'MSE': mse,
            'RMSE': rmse,
            'R2': r2
        }
        
        print("\n模型评估指标：")
        for metric, value in self.metrics.items():
            print(f"{metric}: {value:.4f}")
        
        # 可视化预测结果
        plt.figure(figsize=(12, 6))
        plt.plot(y_test.index, y_test, label='实际销售额')
        plt.plot(y_test.index, y_pred, label='预测销售额')
        plt.title('模型预测效果')
        plt.xlabel('日期')
        plt.ylabel('销售额')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        
        return self.metrics
    
    def make_forecast(self, horizon=7):
        """
        进行销售预测
        """
        if self.model is None:
            raise ValueError("请先训练模型")
        
        if self.data is None:
            raise ValueError("请先加载数据")
        
        # 获取最近的数据用于预测
        last_data = self.data.iloc[-1:].copy()
        
        # 创建预测结果DataFrame
        forecast_dates = pd.date_range(start=self.data.index[-1] + pd.Timedelta(days=1), periods=horizon, freq='D')
        forecast_results = pd.DataFrame(index=forecast_dates)
        
        # 滚动预测
        current_data = last_data.copy()
        
        for i, date in enumerate(forecast_dates):
            # 准备预测特征
            # 注意：这里使用简化的特征准备，实际应用中可能需要更复杂的逻辑
            features = []
            for feature in self.features:
                if feature in current_data.columns:
                    features.append(current_data[feature].iloc[0])
                else:
                    # 对于滞后特征，使用之前的预测值
                    if feature.startswith('sales_lag_'):
                        lag_days = int(feature.split('_')[-1])
                        # 从预测结果中获取滞后数据
                        if lag_days <= i:
                            # 使用之前的预测值
                            if i - lag_days < len(forecast_results):
                                features.append(forecast_results.iloc[i - lag_days]['forecast'])
                            else:
                                # 使用历史数据的最后值
                                features.append(current_data['sales'].iloc[0])
                        else:
                            # 使用历史数据的最后值
                            features.append(current_data['sales'].iloc[0])
                    else:
                        # 对于其他特征，使用默认值或基于规则生成
                        features.append(0 if 'promotion' in feature else 1)
            
            # 进行预测
            forecast_value = self.model.predict([features])[0]
            
            # 存储预测结果
            forecast_results.loc[date, 'forecast'] = forecast_value
            
            # 更新当前数据用于下一次预测
            # 注意：这里是简化实现，实际应用中可能需要更复杂的逻辑来更新特征
            new_data = current_data.copy()
            new_data.index = [date]
            new_data['sales'] = forecast_value
            
            # 更新滞后特征
            for lag in range(1, 8):
                if lag == 1:
                    new_data[f'sales_lag_{lag}'] = current_data['sales'].iloc[0]
                else:
                    new_data[f'sales_lag_{lag}'] = current_data[f'sales_lag_{lag-1}'].iloc[0]
            
            # 更新移动平均特征
            sales_history = [current_data['sales'].iloc[0]]
            if i > 0:
                sales_history.extend(forecast_results['forecast'].iloc[:i])
            
            if len(sales_history) >= 7:
                new_data['sales_ma_7'] = np.mean(sales_history[-7:])
            else:
                new_data['sales_ma_7'] = current_data['sales_ma_7'].iloc[0]
            
            if len(sales_history) >= 30:
                new_data['sales_ma_30'] = np.mean(sales_history[-30:])
            else:
                new_data['sales_ma_30'] = current_data['sales_ma_30'].iloc[0]
            
            current_data = new_data
            
            # 更新日期相关特征
            current_data['day_of_week'] = date.dayofweek
            current_data['is_weekend'] = current_data['day_of_week'].isin([5, 6])
            current_data['month'] = date.month
            current_data['quarter'] = date.quarter
        
        print("\n销售预测结果：")
        print(forecast_results)
        
        # 可视化预测结果
        plt.figure(figsize=(12, 6))
        plt.plot(self.data.index[-30:], self.data['sales'].iloc[-30:], label='历史销售额')
        plt.plot(forecast_results.index, forecast_results['forecast'], label='预测销售额', linestyle='--')
        plt.title('销售预测')
        plt.xlabel('日期')
        plt.ylabel('销售额')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        
        return forecast_results

# 使用示例
if __name__ == "__main__":
    # 创建AI销售预测器实例
    sales_forecaster = AISalesForecaster()
    
    print("正在初始化AI销售预测系统...")
    
    # 加载样本数据
    print("\n加载样本销售数据...")
    sales_forecaster.load_data(sample_data=True, n_samples=365)
    
    # 探索数据
    print("\n探索数据...")
    sales_forecaster.explore_data()
    
    # 预处理数据
    print("\n预处理数据...")
    X_train, X_test, y_train, y_test = sales_forecaster.preprocess_data()
    print(f"训练集大小: {len(X_train)}, 测试集大小: {len(X_test)}")
    
    # 训练模型
    print("\n训练预测模型...")
    sales_forecaster.train_model(X_train, y_train)
    
    # 评估模型
    print("\n评估模型性能...")
    metrics = sales_forecaster.evaluate_model(X_test, y_test)
    
    # 进行销售预测
    print("\n进行销售预测...")
    forecast = sales_forecaster.make_forecast(horizon=14)  # 预测未来14天的销售额
    
    print("\nAI销售预测系统运行完成！")
```

## 高级示例：使用Python实现高级AI销售预测系统
下面是一个更高级的AI销售预测系统实现，包含了更多高级功能，如多模型集成、自动特征选择、异常检测和可视化报告生成等。

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, TimeSeriesSplit, GridSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, VotingRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, mean_absolute_percentage_error
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import xgboost as xgb
import lightgbm as lgb
import warnings
warnings.filterwarnings('ignore')

class AdvancedAISalesForecaster:
    """
    高级AI销售预测系统
    """
    def __init__(self):
        """
        初始化高级销售预测器
        """
        self.models = {}
        self.best_model = None
        self.data = None
        self.raw_data = None
        self.features = None
        self.target = None
        self.metrics = {}
        self.scaler = StandardScaler()
        self.forecast_history = []

    def load_data(self, file_path=None, sample_data=True, n_samples=730):
        """
        加载销售数据
        """
        if sample_data:
            # 生成更复杂的样本销售数据
            dates = pd.date_range(start='2021-01-01', periods=n_samples, freq='D')
            
            # 生成基础销售数据（带趋势和季节性）
            base_sales = 1000 + 2 * np.arange(n_samples)  # 基础趋势
            
            # 添加年、季、月、周季节性
            yearly_seasonal = 200 * np.sin(2 * np.pi * np.arange(n_samples) / 365)  # 年季节性
            quarterly_seasonal = 100 * np.sin(2 * np.pi * np.arange(n_samples) / 90)  # 季季节性
            monthly_seasonal = 50 * np.sin(2 * np.pi * np.arange(n_samples) / 30)  # 月季节性
            weekly_seasonal = 30 * np.sin(2 * np.pi * np.arange(n_samples) / 7)  # 周季节性
            
            # 添加随机噪声
            random_noise = np.random.normal(0, 20, n_samples)  # 随机噪声
            
            # 添加一些随机事件（如促销）
            promotions = np.zeros(n_samples)
            promotion_days = np.random.choice(n_samples, size=int(n_samples * 0.15), replace=False)
            promotions[promotion_days] = 150 + np.random.normal(0, 50, len(promotion_days))
            
            # 添加节假日影响
            holidays = np.zeros(n_samples)
            # 模拟一些节假日（简化实现）
            holiday_indices = [59, 60, 61,  # 春节
                             180, 181,      # 端午节
                             270, 271,      # 中秋节
                             350, 351, 352] # 元旦
            holidays[holiday_indices] = 200
            
            # 添加一些随机的大订单影响
            large_orders = np.zeros(n_samples)
            large_order_days = np.random.choice(n_samples, size=int(n_samples * 0.05), replace=False)
            large_orders[large_order_days] = 300 + np.random.normal(0, 100, len(large_order_days))
            
            # 总销售额
            sales = base_sales + yearly_seasonal + quarterly_seasonal + monthly_seasonal + weekly_seasonal + \
                   random_noise + promotions + holidays + large_orders
            sales = np.maximum(sales, 0)  # 确保销售额非负
            
            # 创建DataFrame
            self.raw_data = pd.DataFrame({
                'date': dates,
                'sales': sales,
                'promotion': promotions > 0,
                'holiday': holidays > 0,
                'large_order': large_orders > 0
            })
            
            # 复制原始数据用于分析
            self.data = self.raw_data.copy()
        else:
            # 从文件加载数据
            if file_path is None:
                raise ValueError("如果不使用样本数据，必须提供文件路径")
            
            # 假设CSV文件包含必要的列
            self.raw_data = pd.read_csv(file_path)
            self.raw_data['date'] = pd.to_datetime(self.raw_data['date'])
            self.data = self.raw_data.copy()
        
        # 设置日期为索引
        self.data.set_index('date', inplace=True)
        
        return self.data

    def data_enrichment(self):
        """
        数据丰富 - 添加更多特征
        """
        if self.data is None:
            raise ValueError("请先加载数据")
        
        df = self.data.copy()
        
        # 添加时间相关特征
        df['day_of_week'] = df.index.dayofweek
        df['is_weekend'] = df['day_of_week'].isin([5, 6])
        df['day_of_month'] = df.index.day
        df['day_of_year'] = df.index.dayofyear
        df['month'] = df.index.month
        df['quarter'] = df.index.quarter
        df['year'] = df.index.year
        
        # 添加滚动统计特征
        window_sizes = [7, 14, 30, 60, 90]
        for window in window_sizes:
            df[f'sales_ma_{window}'] = df['sales'].rolling(window=window).mean()
            df[f'sales_std_{window}'] = df['sales'].rolling(window=window).std()
            df[f'sales_min_{window}'] = df['sales'].rolling(window=window).min()
            df[f'sales_max_{window}'] = df['sales'].rolling(window=window).max()
            df[f'sales_pct_change_{window}'] = df['sales'].pct_change(periods=window)
        
        # 添加滞后特征
        lag_periods = [1, 2, 3, 4, 5, 6, 7, 14, 30]
        for lag in lag_periods:
            df[f'sales_lag_{lag}'] = df['sales'].shift(lag)
        
        # 添加同比和环比特征
        df['sales_yoy'] = df['sales'].pct_change(periods=365)
        df['sales_mom'] = df['sales'].pct_change(periods=30)
        
        # 标记月初、月中、月末
        df['is_month_start'] = df.index.is_month_start.astype(int)
        df['is_month_end'] = df.index.is_month_end.astype(int)
        
        # 经济指标模拟（实际应用中可以接入真实经济数据）
        np.random.seed(42)
        economic_trend = 0.5 + 0.001 * np.arange(len(df)) + 0.1 * np.sin(2 * np.pi * np.arange(len(df)) / 180)
        df['economic_index'] = economic_trend + np.random.normal(0, 0.05, len(df))
        
        # 更新数据
        self.data = df
        
        return self.data

    def detect_anomalies(self, column='sales', method='zscore', threshold=3):
        """
        检测销售数据中的异常值
        """
        if self.data is None:
            raise ValueError("请先加载数据")
        
        df = self.data.copy()
        
        if method == 'zscore':
            # 使用Z-score方法检测异常值
            mean = df[column].mean()
            std = df[column].std()
            df['zscore'] = (df[column] - mean) / std
            df['is_anomaly'] = abs(df['zscore']) > threshold
        elif method == 'iqr':
            # 使用IQR方法检测异常值
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            df['is_anomaly'] = (df[column] < lower_bound) | (df[column] > upper_bound)
        else:
            raise ValueError("不支持的异常检测方法")
        
        # 统计异常值
        anomaly_count = df['is_anomaly'].sum()
        print(f"检测到{anomaly_count}个异常值（{anomaly_count/len(df)*100:.2f}%）")
        
        # 可视化异常值
        plt.figure(figsize=(12, 6))
        plt.plot(df.index, df[column], label='销售额')
        plt.scatter(df[df['is_anomaly']].index, df[df['is_anomaly']][column], 
                   color='red', label='异常值', s=50, alpha=0.5)
        plt.title('销售数据异常值检测')
        plt.xlabel('日期')
        plt.ylabel('销售额')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        
        # 更新数据
        self.data = df
        
        return df[df['is_anomaly']]

    def feature_selection(self, target_column='sales', n_features=20):
        """
        自动特征选择
        """
        if self.data is None:
            raise ValueError("请先加载数据")
        
        # 删除包含NaN的行
        df = self.data.dropna().copy()
        
        # 设置目标变量
        self.target = target_column
        
        # 准备特征和目标
        X = df.select_dtypes(include=[np.number])  # 只选择数值型特征
        if self.target in X.columns:
            X = X.drop([self.target], axis=1)  # 删除目标列
        
        # 排除特殊列
        exclude_columns = ['is_anomaly', 'zscore']
        X = X.drop([col for col in exclude_columns if col in X.columns], axis=1)
        
        y = df[self.target]
        
        # 使用随机森林进行特征重要性评估
        rf = RandomForestRegressor(n_estimators=100, random_state=42)
        rf.fit(X, y)
        
        # 获取特征重要性
        importances = rf.feature_importances_
        indices = np.argsort(importances)[::-1]
        
        # 选择最重要的特征
        selected_features = X.columns[indices][:n_features].tolist()
        
        print(f"\n选择的最重要的{len(selected_features)}个特征：")
        for i, feature in enumerate(selected_features):
            print(f"{i+1}. {feature}: {importances[indices[i]]:.4f}")
        
        # 可视化特征重要性
        plt.figure(figsize=(12, 8))
        plt.title('特征重要性')
        plt.bar(range(min(n_features, 20)), importances[indices][:min(n_features, 20)], 
               align='center')
        plt.xticks(range(min(n_features, 20)), X.columns[indices][:min(n_features, 20)], 
                  rotation=90)
        plt.xlim([-1, min(n_features, 20)])
        plt.tight_layout()
        plt.show()
        
        # 设置选定的特征
        self.features = selected_features
        
        # 准备训练和测试数据
        X_selected = df[self.features]
        
        # 划分训练集和测试集（时间序列数据不随机打乱）
        train_size = int(0.8 * len(X_selected))
        X_train, X_test = X_selected[:train_size], X_selected[train_size:]
        y_train, y_test = y[:train_size], y[train_size:]
        
        # 特征缩放
        self.scaler.fit(X_train)
        X_train_scaled = self.scaler.transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        return X_train_scaled, X_test_scaled, y_train, y_test

    def build_models(self):
        """
        构建多种预测模型
        """
        # 定义多种回归模型
        self.models = {
            'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
            'XGBoost': xgb.XGBRegressor(random_state=42),
            'LightGBM': lgb.LGBMRegressor(random_state=42),
            'Gradient Boosting': GradientBoostingRegressor(random_state=42),
            'KNN': KNeighborsRegressor(n_neighbors=5),
        }
        
        # 创建集成模型
        estimators = [(name, model) for name, model in self.models.items()]
        self.models['Voting Ensemble'] = VotingRegressor(estimators=estimators)
        
        print(f"已构建{len(self.models)}个预测模型")
        
        return self.models

    def train_and_evaluate_models(self, X_train, X_test, y_train, y_test):
        """
        训练和评估所有模型
        """
        if not self.models:
            self.build_models()
        
        # 存储每个模型的评估指标
        all_metrics = {}
        
        # 可视化预测结果
        plt.figure(figsize=(14, 10))
        
        for i, (name, model) in enumerate(self.models.items()):
            print(f"\n训练和评估模型: {name}")
            
            # 训练模型
            model.fit(X_train, y_train)
            
            # 进行预测
            y_pred = model.predict(X_test)
            
            # 计算评估指标
            mae = mean_absolute_error(y_test, y_pred)
            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)
            r2 = r2_score(y_test, y_pred)
            mape = mean_absolute_percentage_error(y_test, y_pred)
            
            # 保存评估指标
            metrics = {
                'MAE': mae,
                'MSE': mse,
                'RMSE': rmse,
                'R2': r2,
                'MAPE': mape
            }
            all_metrics[name] = metrics
            
            print(f"{name}模型评估指标：")
            for metric, value in metrics.items():
                print(f"  {metric}: {value:.4f}")
            
            # 在子图中绘制预测结果（最多显示5个模型）
            if i < 5:
                plt.subplot(3, 2, i+1)
                plt.plot(y_test.index, y_test, label='实际销售额')
                plt.plot(y_test.index, y_pred, label=f'{name}预测')
                plt.title(f'{name}预测结果 (RMSE: {rmse:.2f})')
                plt.xlabel('日期')
                plt.ylabel('销售额')
                plt.legend()
                plt.grid(True)
        
        plt.tight_layout()
        plt.show()
        
        # 选择性能最好的模型（基于RMSE）
        best_model_name = min(all_metrics, key=lambda x: all_metrics[x]['RMSE'])
        self.best_model = self.models[best_model_name]
        
        print(f"\n最佳模型: {best_model_name}")
        print(f"最佳模型性能: {all_metrics[best_model_name]}")
        
        # 保存最佳模型的评估指标
        self.metrics = all_metrics[best_model_name]
        
        return all_metrics, best_model_name

    def hyperparameter_tuning(self, X_train, y_train):
        """
        对最佳模型进行超参数调优
        """
        if self.best_model is None:
            raise ValueError("请先训练和评估模型")
        
        print("\n对最佳模型进行超参数调优...")
        
        # 根据模型类型设置不同的参数网格
        if isinstance(self.best_model, xgb.XGBRegressor):
            param_grid = {
                'n_estimators': [100, 200, 300],
                'max_depth': [3, 5, 7],
                'learning_rate': [0.01, 0.1, 0.3],
                'subsample': [0.8, 1.0],
                'colsample_bytree': [0.8, 1.0]
            }
        elif isinstance(self.best_model, lgb.LGBMRegressor):
            param_grid = {
                'n_estimators': [100, 200, 300],
                'max_depth': [3, 5, 7],
                'learning_rate': [0.01, 0.1, 0.3],
                'subsample': [0.8, 1.0],
                'colsample_bytree': [0.8, 1.0]
            }
        elif isinstance(self.best_model, RandomForestRegressor):
            param_grid = {
                'n_estimators': [100, 200, 300],
                'max_depth': [None, 10, 20, 30],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4]
            }
        else:
            # 对于其他模型，使用简单的参数网格
            param_grid = {
                'n_estimators': [100, 200],
            }
        
        # 使用时间序列交叉验证
        tscv = TimeSeriesSplit(n_splits=5)
        
        # 创建网格搜索对象
        grid_search = GridSearchCV(
            estimator=self.best_model,
            param_grid=param_grid,
            cv=tscv,
            scoring='neg_root_mean_squared_error',
            n_jobs=-1,
            verbose=1
        )
        
        # 执行网格搜索
        grid_search.fit(X_train, y_train)
        
        # 更新最佳模型
        self.best_model = grid_search.best_estimator_
        
        print(f"调优后的最佳参数: {grid_search.best_params_}")
        print(f"调优后的最佳评分: {-grid_search.best_score_:.4f}")
        
        return self.best_model

    def make_advanced_forecast(self, horizon=30, include_confidence=False, confidence_level=0.95):
        """
        进行高级销售预测，支持置信区间估计
        """
        if self.best_model is None:
            raise ValueError("请先训练和评估模型")
        
        if self.data is None:
            raise ValueError("请先加载数据")
        
        # 获取最近的数据用于预测
        df = self.data.dropna().copy()
        last_date = df.index[-1]
        
        # 创建预测结果DataFrame
        forecast_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=horizon, freq='D')
        forecast_results = pd.DataFrame(index=forecast_dates)
        
        # 如果需要置信区间且模型支持，生成置信区间
        if include_confidence and hasattr(self.best_model, 'predict_proba'):
            # 注意：大多数回归模型不直接支持置信区间预测
            # 这里使用简化的方法估计置信区间
            pass
        
        # 滚动预测
        current_data = df.iloc[-1:].copy()
        
        for i, date in enumerate(forecast_dates):
            # 准备预测特征
            features = []
            for feature in self.features:
                if feature in current_data.columns:
                    features.append(current_data[feature].iloc[0])
                else:
                    # 对于滞后特征，使用之前的预测值或历史数据
                    if feature.startswith('sales_lag_'):
                        lag_days = int(feature.split('_')[-1])
                        # 从预测结果或历史数据中获取滞后数据
                        if lag_days <= i:
                            # 使用之前的预测值
                            if i - lag_days < len(forecast_results):
                                features.append(forecast_results.iloc[i - lag_days]['forecast'])
                            else:
                                # 使用历史数据的最后值
                                features.append(current_data['sales'].iloc[0])
                        else:
                            # 计算需要回溯的天数
                            back_days = lag_days - i
                            if back_days <= len(df):
                                # 使用历史数据
                                features.append(df.iloc[-back_days]['sales'])
                            else:
                                # 使用默认值
                                features.append(df['sales'].mean())
                    # 对于移动平均特征，使用最近的销售数据计算
                    elif feature.startswith('sales_ma_'):
                        window = int(feature.split('_')[-1])
                        # 收集最近的销售数据
                        recent_sales = []
                        # 添加历史数据
                        if len(df) >= window - i:
                            recent_sales.extend(df['sales'].iloc[-(window - i):].tolist())
                        else:
                            recent_sales.extend(df['sales'].tolist())
                        # 添加已预测的数据
                        recent_sales.extend(forecast_results['forecast'].iloc[:i].tolist())
                        # 计算移动平均
                        if len(recent_sales) >= window:
                            features.append(np.mean(recent_sales[-window:]))
                        else:
                            features.append(np.mean(recent_sales))
                    # 对于标准差特征，使用最近的销售数据计算
                    elif feature.startswith('sales_std_'):
                        window = int(feature.split('_')[-1])
                        # 收集最近的销售数据
                        recent_sales = []
                        # 添加历史数据
                        if len(df) >= window - i:
                            recent_sales.extend(df['sales'].iloc[-(window - i):].tolist())
                        else:
                            recent_sales.extend(df['sales'].tolist())
                        # 添加已预测的数据
                        recent_sales.extend(forecast_results['forecast'].iloc[:i].tolist())
                        # 计算标准差
                        if len(recent_sales) >= window:
                            features.append(np.std(recent_sales[-window:]))
                        else:
                            features.append(np.std(recent_sales))
                    # 对于百分比变化特征，使用最近的销售数据计算
                    elif feature.startswith('sales_pct_change_'):
                        window = int(feature.split('_')[-1])
                        # 收集最近的销售数据
                        recent_sales = []
                        # 添加历史数据
                        if len(df) >= window + 1 - i:
                            recent_sales.extend(df['sales'].iloc[-(window + 1 - i):].tolist())
                        else:
                            recent_sales.extend(df['sales'].tolist())
                        # 添加已预测的数据
                        recent_sales.extend(forecast_results['forecast'].iloc[:i].tolist())
                        # 计算百分比变化
                        if len(recent_sales) >= window + 1:
                            pct_change = (recent_sales[-1] - recent_sales[-window-1]) / recent_sales[-window-1]
                            features.append(pct_change)
                        else:
                            features.append(0)
                    # 对于同比特征
                    elif feature == 'sales_yoy':
                        # 检查是否有去年同期的数据
                        if len(df) >= 365:
                            # 使用去年同期的销售数据计算同比
                            features.append((forecast_results['forecast'].iloc[i-1] if i > 0 else df['sales'].iloc[-1] - df['sales'].iloc[-365]) / df['sales'].iloc[-365])
                        else:
                            features.append(0)
                    # 对于环比特征
                    elif feature == 'sales_mom':
                        # 检查是否有上月同期的数据
                        if len(df) >= 30:
                            # 使用上月同期的销售数据计算环比
                            features.append((forecast_results['forecast'].iloc[i-1] if i > 0 else df['sales'].iloc[-1] - df['sales'].iloc[-30]) / df['sales'].iloc[-30])
                        else:
                            features.append(0)
                    # 对于时间相关特征
                    elif feature == 'day_of_week':
                        features.append(date.dayofweek)
                    elif feature == 'is_weekend':
                        features.append(int(date.dayofweek in [5, 6]))
                    elif feature == 'day_of_month':
                        features.append(date.day)
                    elif feature == 'day_of_year':
                        features.append(date.dayofyear)
                    elif feature == 'month':
                        features.append(date.month)
                    elif feature == 'quarter':
                        features.append(date.quarter)
                    elif feature == 'year':
                        features.append(date.year)
                    elif feature == 'is_month_start':
                        features.append(int(date.is_month_start))
                    elif feature == 'is_month_end':
                        features.append(int(date.is_month_end))
                    # 对于经济指标特征
                    elif feature == 'economic_index':
                        # 使用简单的趋势预测经济指标
                        last_economic_index = df['economic_index'].iloc[-1]
                        # 假设经济指标有轻微的上升趋势
                        features.append(last_economic_index + 0.001 * (i + 1) + np.random.normal(0, 0.02))
                    # 对于其他特征，使用默认值
                    else:
                        # 检查是否是布尔型特征
                        if feature in ['promotion', 'holiday', 'large_order']:
                            # 这里使用简化的方法，实际应用中应该基于历史模式或外部数据
                            features.append(0)  # 默认假设没有促销、节假日或大订单
                        else:
                            # 使用该特征的平均值
                            if feature in df.columns:
                                features.append(df[feature].mean())
                            else:
                                features.append(0)
            
            # 特征缩放
            features_scaled = self.scaler.transform([features])
            
            # 进行预测
            forecast_value = self.best_model.predict(features_scaled)[0]
            
            # 存储预测结果
            forecast_results.loc[date, 'forecast'] = max(0, forecast_value)  # 确保预测值非负
            
            # 更新当前数据用于下一次预测
            new_data = current_data.copy()
            new_data.index = [date]
            new_data['sales'] = forecast_value
            
            # 更新时间相关特征
            new_data['day_of_week'] = date.dayofweek
            new_data['is_weekend'] = int(date.dayofweek in [5, 6])
            new_data['day_of_month'] = date.day
            new_data['day_of_year'] = date.dayofyear
            new_data['month'] = date.month
            new_data['quarter'] = date.quarter
            new_data['year'] = date.year
            new_data['is_month_start'] = int(date.is_month_start)
            new_data['is_month_end'] = int(date.is_month_end)
            
            current_data = new_data
        
        # 保存预测历史
        self.forecast_history.append(forecast_results)
        
        # 可视化预测结果
        plt.figure(figsize=(14, 8))
        
        # 绘制历史数据
        plt.plot(df.index[-90:], df['sales'].iloc[-90:], label='历史销售额')
        
        # 绘制预测结果
        plt.plot(forecast_results.index, forecast_results['forecast'], 
                label='预测销售额', linestyle='--', color='red')
        
        # 如果有置信区间，绘制置信区间
        if include_confidence and 'lower_bound' in forecast_results.columns and 'upper_bound' in forecast_results.columns:
            plt.fill_between(forecast_results.index, 
                            forecast_results['lower_bound'], 
                            forecast_results['upper_bound'], 
                            alpha=0.2, color='red', label=f'{confidence_level*100}% 置信区间')
        
        plt.title('高级销售预测')
        plt.xlabel('日期')
        plt.ylabel('销售额')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        
        return forecast_results

    def generate_forecast_report(self, forecast_results):
        """
        生成预测报告
        """
        if forecast_results is None:
            raise ValueError("请先进行预测")
        
        report = {
            'forecast_summary': {
                'start_date': forecast_results.index[0].strftime('%Y-%m-%d'),
                'end_date': forecast_results.index[-1].strftime('%Y-%m-%d'),
                'total_forecast': forecast_results['forecast'].sum(),
                'average_daily_forecast': forecast_results['forecast'].mean(),
                'max_forecast_day': forecast_results['forecast'].idxmax().strftime('%Y-%m-%d'),
                'max_forecast_value': forecast_results['forecast'].max(),
                'min_forecast_day': forecast_results['forecast'].idxmin().strftime('%Y-%m-%d'),
                'min_forecast_value': forecast_results['forecast'].min()
            },
            'model_performance': self.metrics,
            'forecast_details': forecast_results.to_dict()['forecast']
        }
        
        print("\n===== 销售预测报告 =====")
        print(f"预测期间: {report['forecast_summary']['start_date']} 至 {report['forecast_summary']['end_date']}")
        print(f"预测总销售额: {report['forecast_summary']['total_forecast']:.2f}")
        print(f"平均日销售额预测: {report['forecast_summary']['average_daily_forecast']:.2f}")
        print(f"最高预测日: {report['forecast_summary']['max_forecast_day']} ({report['forecast_summary']['max_forecast_value']:.2f})")
        print(f"最低预测日: {report['forecast_summary']['min_forecast_day']} ({report['forecast_summary']['min_forecast_value']:.2f})")
        print("\n模型性能指标:")
        for metric, value in report['model_performance'].items():
            print(f"  {metric}: {value:.4f}")
        print("====================")
        
        return report

    def generate_visualization_report(self):
        """
        生成可视化报告
        """
        if self.data is None:
            raise ValueError("请先加载数据")
        
        df = self.data.dropna().copy()
        
        # 创建一个包含多个子图的图表
        fig = plt.figure(figsize=(20, 20))
        
        # 1. 销售趋势图
        ax1 = plt.subplot(4, 2, 1)
        ax1.plot(df.index, df['sales'])
        ax1.set_title('销售趋势')
        ax1.set_xlabel('日期')
        ax1.set_ylabel('销售额')
        ax1.grid(True)
        
        # 2. 季节性分解图
        try:
            result = seasonal_decompose(df['sales'], model='additive', period=30)  # 假设月季节性
            ax2 = plt.subplot(4, 2, 2)
            result.seasonal.plot(ax=ax2)
            ax2.set_title('销售季节性')
            ax2.set_xlabel('日期')
            ax2.set_ylabel('季节性成分')
            ax2.grid(True)
        except Exception as e:
            print(f"季节性分解失败：{e}")
        
        # 3. 月度销售额分布图
        ax3 = plt.subplot(4, 2, 3)
        monthly_sales = df.groupby('month')['sales'].mean()
        ax3.bar(monthly_sales.index, monthly_sales.values)
        ax3.set_title('月度平均销售额')
        ax3.set_xlabel('月份')
        ax3.set_ylabel('平均销售额')
        ax3.grid(True, axis='y')
        
        # 4. 周销售额分布图
        ax4 = plt.subplot(4, 2, 4)
        weekly_sales = df.groupby('day_of_week')['sales'].mean()
        ax4.bar(weekly_sales.index, weekly_sales.values)
        ax4.set_title('周平均销售额')
        ax4.set_xlabel('星期几')
        ax4.set_ylabel('平均销售额')
        ax4.set_xticks(range(7))
        ax4.set_xticklabels(['周一', '周二', '周三', '周四', '周五', '周六', '周日'])
        ax4.grid(True, axis='y')
        
        # 5. 销售分布直方图
        ax5 = plt.subplot(4, 2, 5)
        ax5.hist(df['sales'], bins=30, alpha=0.7)
        ax5.set_title('销售额分布')
        ax5.set_xlabel('销售额')
        ax5.set_ylabel('频数')
        ax5.grid(True, axis='y')
        
        # 6. 促销活动对销售的影响
        if 'promotion' in df.columns:
            ax6 = plt.subplot(4, 2, 6)
            promotion_effect = df.groupby('promotion')['sales'].mean()
            ax6.bar(promotion_effect.index, promotion_effect.values)
            ax6.set_title('促销活动对销售额的影响')
            ax6.set_xlabel('是否有促销')
            ax6.set_ylabel('平均销售额')
            ax6.set_xticks([0, 1])
            ax6.set_xticklabels(['无促销', '有促销'])
            ax6.grid(True, axis='y')
        
        # 7. 销售额与经济指标的关系
        if 'economic_index' in df.columns:
            ax7 = plt.subplot(4, 2, 7)
            ax7.scatter(df['economic_index'], df['sales'], alpha=0.5)
            ax7.set_title('销售额与经济指标的关系')
            ax7.set_xlabel('经济指标')
            ax7.set_ylabel('销售额')
            ax7.grid(True)
        
        # 8. 特征重要性热图（如果已经选择了特征）
        if self.features:
            ax8 = plt.subplot(4, 2, 8)
            # 获取特征相关性矩阵（仅选择前10个特征）
            corr_cols = ['sales'] + self.features[:9]  # 加上目标变量和前9个特征
            corr_cols = [col for col in corr_cols if col in df.columns]
            corr_matrix = df[corr_cols].corr()
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax8)
            ax8.set_title('特征相关性热图')
        
        plt.tight_layout()
        plt.show()

# 使用示例
if __name__ == "__main__":
    # 创建高级AI销售预测器实例
    advanced_sales_forecaster = AdvancedAISalesForecaster()
    
    print("正在初始化高级AI销售预测系统...")
    
    # 加载样本数据
    print("\n加载样本销售数据...")
    advanced_sales_forecaster.load_data(sample_data=True, n_samples=730)  # 加载2年的样本数据
    
    # 数据丰富
    print("\n进行数据丰富...")
    advanced_sales_forecaster.data_enrichment()
    
    # 异常检测
    print("\n检测销售数据异常值...")
    anomalies = advanced_sales_forecaster.detect_anomalies()
    
    # 特征选择
    print("\n进行自动特征选择...")
    X_train_scaled, X_test_scaled, y_train, y_test = advanced_sales_forecaster.feature_selection(n_features=20)
    
    # 构建多种预测模型
    print("\n构建多种预测模型...")
    models = advanced_sales_forecaster.build_models()
    
    # 训练和评估模型
    print("\n训练和评估所有模型...")
    all_metrics, best_model_name = advanced_sales_forecaster.train_and_evaluate_models(
        X_train_scaled, X_test_scaled, y_train, y_test
    )
    
    # 超参数调优
    print("\n对最佳模型进行超参数调优...")
    best_model = advanced_sales_forecaster.hyperparameter_tuning(X_train_scaled, y_train)
    
    # 进行高级销售预测
    print("\n进行高级销售预测...")
    forecast_results = advanced_sales_forecaster.make_advanced_forecast(horizon=30)  # 预测未来30天的销售额
    
    # 生成预测报告
    print("\n生成销售预测报告...")
    report = advanced_sales_forecaster.generate_forecast_report(forecast_results)
    
    # 生成可视化报告
    print("\n生成可视化报告...")
    advanced_sales_forecaster.generate_visualization_report()
    
    print("\n高级AI销售预测系统运行完成！")