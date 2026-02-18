# 音频增强

AI音频增强是利用人工智能技术对音频信号进行处理和优化，以改善其质量、清晰度和可听性的过程。随着深度学习和信号处理技术的快速发展，AI音频增强已经成为音频处理领域的重要工具，能够有效地解决噪声消除、语音增强、音频修复、音质提升等问题。这些技术广泛应用于音频录制、语音通信、内容制作、音乐产业、安防监控等多个领域。本章将介绍AI音频增强的基本原理、主要应用场景以及详细的使用示例，帮助你掌握如何使用AI进行音频增强。

## AI音频增强的基本原理

AI音频增强的核心是让计算机能够理解音频信号的特性，并应用相应的算法来改善其质量。现代AI音频增强主要基于深度学习和数字信号处理技术。

### 主要类型

- **噪声消除（Noise Reduction）**：去除背景噪声，保留目标声音
- **语音增强（Speech Enhancement）**：提高语音的清晰度和可懂度
- **音频修复（Audio Restoration）**：修复受损或失真的音频
- **音质提升（Audio Quality Enhancement）**：提高音频的整体质量
- **混音分离（Source Separation）**：将混合音频分离为不同的音源
- **音频均衡（Audio Equalization）**：调整音频的频率响应
- **动态范围压缩（Dynamic Range Compression）**：控制音频的动态范围
- **空间音频增强（Spatial Audio Enhancement）**：改善音频的空间特性

### 核心技术原理

#### 音频信号表示

在AI音频增强中，音频信号需要以适合机器学习模型处理的方式进行表示，常见的表示方法包括：

1. **时域表示**：
   - 波形（Waveform）：直接表示音频信号的振幅随时间的变化
   - 采样数据（Sampled Data）：离散化的音频采样点
   - 短时能量（Short-time Energy）：窗口化的能量计算
   - 过零率（Zero Crossing Rate）：信号穿过零值的次数

2. **频域表示**：
   - 短时傅里叶变换（STFT）：分析短时间窗口内的频谱内容
   - 梅尔谱图（Mel Spectrogram）：模拟人类听觉系统的频谱表示
   - 语谱图（Spectrogram）：声音的时频表示
   - 功率谱（Power Spectrum）：表示信号在不同频率上的功率

3. **时频域表示**：
   - 连续小波变换（CWT）：适合分析非平稳信号
   - 常数Q变换（Constant-Q Transform）：适合音乐分析
   - 小波包变换（Wavelet Packet Transform）：提供更精细的频率分解

#### 深度学习在音频增强中的应用

深度学习模型在音频增强中取得了显著成功，主要包括以下几种模型：

- **卷积神经网络（CNN）**：擅长处理局部特征，适用于频谱图增强
- **循环神经网络（RNN）**：擅长处理序列数据，适用于时域音频增强
- **长短期记忆网络（LSTM）**：解决长序列依赖问题，适用于复杂音频处理
- **生成对抗网络（GANs）**：如CycleGAN，通过对抗训练生成高质量音频
- **自编码器（Autoencoders）**：用于特征学习和降噪
- **Transformer模型**：利用自注意力机制，在复杂音频任务中表现出色
- **分离模型（Separation Models）**：如ConvTasNet、Wave-U-Net，用于音源分离

#### 音频增强流程

AI音频增强的基本流程包括以下几个步骤：

1. **音频采集**：获取原始音频信号
2. **预处理**：对音频进行分段、归一化等处理
3. **特征提取**：提取音频的时域、频域或时频域特征
4. **增强模型**：使用训练好的深度学习模型进行处理
5. **后处理**：对增强后的音频进行进一步优化
6. **评估**：评估增强后的音频质量
7. **输出**：以合适的格式保存或播放增强后的音频

## AI音频增强的应用场景

AI音频增强技术已经广泛应用于各个领域，以下是一些常见的应用场景：

### 1. 语音通信
- 电话会议噪声消除
- 语音通话质量提升
- 网络语音传输优化
- 移动设备通话降噪
- 视频会议音频增强

### 2. 内容制作与媒体
- 录音棚音频后期处理
- 播客和有声读物制作
- 视频内容音频增强
- 音乐母带处理
- 现场录音改善

### 3. 安防监控
- 监控音频清晰度提升
- 远距离语音增强
- 嘈杂环境中的语音识别
- 异常声音检测前处理
- 执法记录仪音频优化

### 4. 医疗健康
- 助听器信号处理
- 医疗诊断音频分析
- 远程医疗音频质量保证
- 语音障碍治疗辅助
- 睡眠监测音频处理

### 5. 教育与培训
- 在线课程音频优化
- 教学录音质量提升
- 语言学习音频处理
- 课堂录音降噪
- 教育内容音频增强

### 6. 智能家居与物联网
- 智能音箱语音识别优化
- 家庭安防音频处理
- 环境声音监测
- 语音控制信号增强
- 智能家居设备音频交互

### 7. 汽车与交通
- 车载语音系统降噪
- 车内通话质量提升
- 车辆状态监测音频处理
- 交通监控音频增强
- 自动驾驶音频感知

### 8. 工业与工程
- 设备故障检测音频处理
- 工业环境语音通信
- 管道泄漏检测音频增强
- 机械设备状态监测
- 工业安全音频监控

## 详细使用示例

### 噪声消除

**功能说明**：去除音频中的背景噪声，如环境噪音、电子设备噪音、风声等，同时保留目标声音（如语音）的清晰度和可懂度。

**使用示例**：

```
# 噪声消除示例
输入：一段包含背景噪音的语音录音
输出：一段背景噪音被消除的清晰语音
```

**实际应用**：

```python
# 使用noisereduce库进行音频噪声消除
import noisereduce as nr
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import os

# 设置中文字体以支持中文显示
plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]

class AudioNoiseReducer:
    def __init__(self):
        print("初始化音频噪声消除系统...")
        # 设置默认参数
        self.sample_rate = 22050  # 采样率
    
    def load_audio(self, audio_path):
        """加载音频文件"""
        try:
            audio, sr = librosa.load(audio_path, sr=self.sample_rate)
            print(f"加载音频文件: {audio_path}")
            print(f"音频长度: {len(audio)/sr:.2f}秒, 采样率: {sr}Hz")
            return audio, sr
        except Exception as e:
            print(f"无法加载音频文件: {e}")
            return None, None
    
    def save_audio(self, audio, sr, filename="denoised_audio.wav"):
        """保存音频文件"""
        try:
            sf.write(filename, audio, sr)
            print(f"音频已保存到: {filename}")
            return filename
        except Exception as e:
            print(f"音频保存失败: {e}")
            return None
    
    def extract_noise_sample(self, audio, sr, noise_start=0, noise_duration=1):
        """从音频中提取噪声样本"""
        try:
            noise_end = noise_start + noise_duration
            noise_sample = audio[int(noise_start*sr):int(noise_end*sr)]
            print(f"提取噪声样本: 时间范围 {noise_start}-{noise_end}秒")
            return noise_sample
        except Exception as e:
            print(f"提取噪声样本失败: {e}")
            return None
    
    def reduce_noise(self, audio, sr, noise_sample=None, **kwargs):
        """执行噪声消除"""
        try:
            print("执行噪声消除...")
            
            # 默认参数
            params = {
                'prop_decrease': 1.0,    # 噪声减少比例
                'n_fft': 2048,           # FFT窗口大小
                'win_length': 2048,      # 窗口长度
                'hop_length': 512,       # 跳跃长度
                'n_std_thresh': 1.5,     # 噪声检测的标准差阈值
                'stationary': False      # 噪声是否平稳
            }
            
            # 更新用户提供的参数
            params.update(kwargs)
            
            # 执行噪声消除
            if noise_sample is not None:
                # 使用指定的噪声样本
                denoised_audio = nr.reduce_noise(
                    y=audio,
                    sr=sr,
                    y_noise=noise_sample,
                    **params
                )
            else:
                # 让算法自动检测噪声
                denoised_audio = nr.reduce_noise(
                    y=audio,
                    sr=sr,
                    **params
                )
            
            print("噪声消除完成！")
            return denoised_audio
        except Exception as e:
            print(f"噪声消除失败: {e}")
            return None
    
    def visualize_audio_comparison(self, original_audio, denoised_audio, sr):
        """可视化原始音频和降噪后音频的对比"""
        try:
            plt.figure(figsize=(16, 12))
            
            # 绘制原始音频波形
            plt.subplot(3, 2, 1)
            librosa.display.waveshow(original_audio, sr=sr)
            plt.title('原始音频波形')
            plt.xlabel('时间 (秒)')
            plt.ylabel('振幅')
            
            # 绘制降噪后音频波形
            plt.subplot(3, 2, 2)
            librosa.display.waveshow(denoised_audio, sr=sr)
            plt.title('降噪后音频波形')
            plt.xlabel('时间 (秒)')
            plt.ylabel('振幅')
            
            # 绘制原始音频梅尔谱图
            plt.subplot(3, 2, 3)
            S_original = librosa.feature.melspectrogram(y=original_audio, sr=sr, n_mels=128)
            S_dB_original = librosa.power_to_db(S_original, ref=np.max)
            librosa.display.specshow(S_dB_original, x_axis='time', y_axis='mel', sr=sr, fmax=8000)
            plt.colorbar(format='%+2.0f dB')
            plt.title('原始音频梅尔谱图')
            
            # 绘制降噪后音频梅尔谱图
            plt.subplot(3, 2, 4)
            S_denoised = librosa.feature.melspectrogram(y=denoised_audio, sr=sr, n_mels=128)
            S_dB_denoised = librosa.power_to_db(S_denoised, ref=np.max)
            librosa.display.specshow(S_dB_denoised, x_axis='time', y_axis='mel', sr=sr, fmax=8000)
            plt.colorbar(format='%+2.0f dB')
            plt.title('降噪后音频梅尔谱图')
            
            # 绘制频谱差异
            plt.subplot(3, 1, 3)
            freq_bins = np.linspace(0, sr/2, S_original.shape[0])
            original_mean_spec = np.mean(S_dB_original, axis=1)
            denoised_mean_spec = np.mean(S_dB_denoised, axis=1)
            
            plt.plot(freq_bins/1000, original_mean_spec, label='原始音频')
            plt.plot(freq_bins/1000, denoised_mean_spec, label='降噪后音频')
            plt.title('频谱对比')
            plt.xlabel('频率 (kHz)')
            plt.ylabel('分贝 (dB)')
            plt.legend()
            plt.grid(True)
            
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            print(f"音频可视化失败: {e}")
    
    def batch_denoise(self, audio_paths, output_dir=".", **kwargs):
        """批量处理音频文件"""
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        results = []
        
        for audio_path in audio_paths:
            if os.path.exists(audio_path):
                # 获取文件名
                filename = os.path.basename(audio_path)
                name_without_ext = os.path.splitext(filename)[0]
                
                print(f"\n处理文件: {filename}")
                
                # 加载音频
                audio, sr = self.load_audio(audio_path)
                
                if audio is not None:
                    # 执行噪声消除
                    denoised_audio = self.reduce_noise(audio, sr, **kwargs)
                    
                    if denoised_audio is not None:
                        # 保存处理后的音频
                        output_path = os.path.join(output_dir, f"denoised_{filename}")
                        saved_file = self.save_audio(denoised_audio, sr, output_path)
                        
                        if saved_file:
                            results.append({
                                'input_file': audio_path,
                                'output_file': saved_file
                            })
            else:
                print(f"文件不存在: {audio_path}")
        
        print(f"\n批量处理完成，共处理 {len(results)} 个文件")
        return results

# 使用示例
if __name__ == "__main__":
    # 创建噪声消除实例
    noise_reducer = AudioNoiseReducer()
    
    # 示例1：处理单个音频文件
    print("\n=== 示例1：处理单个音频文件 ===")
    
    # 音频文件路径
    audio_path = "noisy_audio.wav"
    
    # 检查文件是否存在
    if os.path.exists(audio_path):
        # 加载音频
        audio, sr = noise_reducer.load_audio(audio_path)
        
        if audio is not None:
            # 方法1：自动检测噪声
            print("\n方法1：自动检测噪声")
            denoised_audio_auto = noise_reducer.reduce_noise(audio, sr)
            
            if denoised_audio_auto is not None:
                # 保存降噪后的音频
                output_file_auto = "denoised_auto.wav"
                noise_reducer.save_audio(denoised_audio_auto, sr, output_file_auto)
                
                # 可视化对比
                noise_reducer.visualize_audio_comparison(audio, denoised_audio_auto, sr)
            
            # 方法2：使用指定的噪声样本
            print("\n方法2：使用指定的噪声样本")
            # 假设音频的前1秒是纯噪声
            noise_sample = noise_reducer.extract_noise_sample(audio, sr, noise_start=0, noise_duration=1)
            
            if noise_sample is not None:
                denoised_audio_manual = noise_reducer.reduce_noise(audio, sr, noise_sample=noise_sample)
                
                if denoised_audio_manual is not None:
                    # 保存降噪后的音频
                    output_file_manual = "denoised_manual.wav"
                    noise_reducer.save_audio(denoised_audio_manual, sr, output_file_manual)
    else:
        print(f"文件不存在: {audio_path}")
        print("请提供有效的音频文件路径")
    
    # 示例2：批量处理多个音频文件
    print("\n=== 示例2：批量处理多个音频文件 ===")
    
    # 音频文件列表（需要替换为实际文件路径）
    audio_files = ["noisy_audio1.wav", "noisy_audio2.wav"]  # 示例文件
    valid_files = [f for f in audio_files if os.path.exists(f)]
    
    if valid_files:
        # 批量处理
        batch_results = noise_reducer.batch_denoise(valid_files, output_dir="denoised_output")
    else:
        print("没有找到有效的音频文件进行批量处理")
    
    print("\n音频噪声消除处理完成！")
```

### 混音分离

**功能说明**：将混合的音频信号分离为不同的音源，如将一段包含人声、背景音乐和其他声音的混合音频分离为人声轨道、伴奏轨道等。

**使用示例**：

```
# 混音分离示例
输入：一段包含人声和背景音乐的混合音频
输出：分离后的人声轨道和背景音乐轨道
```

**实际应用**：

```python
# 使用Spleeter进行音频混音分离
import os
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
import soundfile as sf
from spleeter.separator import Separator
import warnings

# 忽略警告信息
warnings.filterwarnings("ignore")

# 设置中文字体以支持中文显示
plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]

class AudioSourceSeparator:
    def __init__(self, model_type='spleeter:2stems'):
        """
        初始化音频分离系统
        model_type: 分离模型类型，可选值：
            - 'spleeter:2stems': 分离为 vocals 和 accompaniment
            - 'spleeter:4stems': 分离为 vocals, drums, bass, other
            - 'spleeter:5stems': 分离为 vocals, drums, bass, piano, other
        """
        print("初始化音频混音分离系统...")
        self.model_type = model_type
        self.separator = Separator(model_type)
        print(f"使用模型: {model_type}")
    
    def separate_audio(self, audio_path, output_dir="./separated"):
        """执行音频分离"""
        try:
            if not os.path.exists(audio_path):
                print(f"文件不存在: {audio_path}")
                return None
            
            print(f"开始分离音频: {audio_path}")
            print(f"输出目录: {output_dir}")
            
            # 创建输出目录
            os.makedirs(output_dir, exist_ok=True)
            
            # 执行分离
            self.separator.separate_to_file(audio_path, output_dir)
            
            print("音频分离完成！")
            
            # 返回分离后的文件路径
            base_filename = os.path.splitext(os.path.basename(audio_path))[0]
            separated_files = self._get_separated_files(output_dir, base_filename)
            
            return separated_files
        except Exception as e:
            print(f"音频分离失败: {e}")
            return None
    
    def _get_separated_files(self, output_dir, base_filename):
        """获取分离后的文件路径"""
        separated_files = {}
        output_subdir = os.path.join(output_dir, base_filename)
        
        if os.path.exists(output_subdir):
            # 根据模型类型确定可能的音轨名称
            if self.model_type == 'spleeter:2stems':
                stems = ['vocals', 'accompaniment']
            elif self.model_type == 'spleeter:4stems':
                stems = ['vocals', 'drums', 'bass', 'other']
            elif self.model_type == 'spleeter:5stems':
                stems = ['vocals', 'drums', 'bass', 'piano', 'other']
            else:
                stems = []
            
            # 查找分离后的文件
            for stem in stems:
                file_path = os.path.join(output_subdir, f'{stem}.wav')
                if os.path.exists(file_path):
                    separated_files[stem] = file_path
                    print(f"找到分离后的文件: {stem} -> {file_path}")
            
            # 查找所有WAV文件（以防模型输出不同的命名）
            for file in os.listdir(output_subdir):
                if file.endswith('.wav'):
                    stem_name = os.path.splitext(file)[0]
                    if stem_name not in separated_files:
                        file_path = os.path.join(output_subdir, file)
                        separated_files[stem_name] = file_path
                        print(f"找到额外的分离文件: {stem_name} -> {file_path}")
        
        return separated_files
    
    def load_audio(self, audio_path):
        """加载音频文件"""
        try:
            audio, sr = librosa.load(audio_path, sr=None)
            return audio, sr
        except Exception as e:
            print(f"无法加载音频文件: {e}")
            return None, None
    
    def visualize_source_separation(self, original_path, separated_files):
        """可视化混音分离结果"""
        try:
            # 加载原始音频
            original_audio, original_sr = self.load_audio(original_path)
            
            if original_audio is None:
                return
            
            # 确定要显示的音轨数量
            n_tracks = len(separated_files) + 1  # 原始音频 + 分离的音轨
            
            plt.figure(figsize=(16, 4 * n_tracks))
            
            # 绘制原始音频波形
            plt.subplot(n_tracks, 1, 1)
            librosa.display.waveshow(original_audio, sr=original_sr)
            plt.title('原始混合音频')
            plt.xlabel('时间 (秒)')
            plt.ylabel('振幅')
            
            # 绘制每个分离的音轨
            for i, (stem_name, file_path) in enumerate(separated_files.items(), 2):
                stem_audio, stem_sr = self.load_audio(file_path)
                
                if stem_audio is not None:
                    plt.subplot(n_tracks, 1, i)
                    librosa.display.waveshow(stem_audio, sr=stem_sr)
                    plt.title(f'分离的音轨: {stem_name}')
                    plt.xlabel('时间 (秒)')
                    plt.ylabel('振幅')
            
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            print(f"音频可视化失败: {e}")
    
    def batch_separate(self, audio_paths, output_dir="./separated_batch"):
        """批量分离音频文件"""
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        results = []
        
        for audio_path in audio_paths:
            if os.path.exists(audio_path):
                # 获取文件名
                filename = os.path.basename(audio_path)
                print(f"\n处理文件: {filename}")
                
                # 创建每个文件的输出子目录
                base_filename = os.path.splitext(filename)[0]
                file_output_dir = os.path.join(output_dir, base_filename)
                
                # 执行分离
                separated_files = self.separate_audio(audio_path, file_output_dir)
                
                if separated_files:
                    results.append({
                        'input_file': audio_path,
                        'separated_files': separated_files
                    })
            else:
                print(f"文件不存在: {audio_path}")
        
        print(f"\n批量分离完成，共处理 {len(results)} 个文件")
        return results
    
    def compare_separation_models(self, audio_path, output_dir="./model_comparison"):
        """比较不同分离模型的效果"""
        print("比较不同分离模型的效果...")
        
        # 支持的模型类型
        model_types = ['spleeter:2stems', 'spleeter:4stems', 'spleeter:5stems']
        
        results = {}
        
        for model_type in model_types:
            print(f"\n使用模型: {model_type}")
            
            # 创建该模型的输出目录
            model_output_dir = os.path.join(output_dir, model_type.replace(':', '_'))
            
            # 创建新的分离器
            temp_separator = AudioSourceSeparator(model_type)
            
            # 执行分离
            separated_files = temp_separator.separate_audio(audio_path, model_output_dir)
            
            if separated_files:
                results[model_type] = {
                    'output_dir': model_output_dir,
                    'separated_files': separated_files
                }
        
        print("\n模型比较完成！")
        return results

# 使用示例
if __name__ == "__main__":
    # 示例1：使用2stems模型分离人声和伴奏
    print("\n=== 示例1：分离人声和伴奏 ===")
    
    # 创建分离器实例（2stems: 人声和伴奏）
    separator_2stems = AudioSourceSeparator('spleeter:2stems')
    
    # 音频文件路径
    audio_path = "mixed_audio.wav"
    
    # 检查文件是否存在
    if os.path.exists(audio_path):
        # 执行分离
        separated_files = separator_2stems.separate_audio(audio_path, "./separated_2stems")
        
        if separated_files:
            # 可视化分离结果
            separator_2stems.visualize_source_separation(audio_path, separated_files)
            
            # 打印分离后的文件信息
            print("分离后的文件:")
            for stem_name, file_path in separated_files.items():
                print(f"- {stem_name}: {file_path}")
    else:
        print(f"文件不存在: {audio_path}")
        print("请提供有效的音频文件路径")
    
    # 示例2：使用4stems模型分离为多个音轨
    print("\n=== 示例2：分离为多轨（人声、鼓、贝斯、其他） ===")
    
    if os.path.exists(audio_path):
        # 创建分离器实例（4stems: 人声、鼓、贝斯、其他）
        separator_4stems = AudioSourceSeparator('spleeter:4stems')
        
        # 执行分离
        separated_files_4stems = separator_4stems.separate_audio(audio_path, "./separated_4stems")
        
        if separated_files_4stems:
            # 打印分离后的文件信息
            print("分离后的多轨文件:")
            for stem_name, file_path in separated_files_4stems.items():
                print(f"- {stem_name}: {file_path}")
    
    print("\n音频混音分离处理完成！")
```

### 音质提升

**功能说明**：提高低质量音频的音质，包括提升清晰度、增强低音、修复失真、增加空间感等。

**使用示例**：

```
# 音质提升示例
输入：一段低质量的音频录音（有杂音、失真、音质差）
输出：一段音质明显改善的音频
```

**实际应用**：

```python
# 使用LibROSA和PyTorch进行音频音质提升
import os
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
import soundfile as sf
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import warnings

# 忽略警告信息
warnings.filterwarnings("ignore")

# 设置中文字体以支持中文显示
plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]

# 定义简单的音频增强网络
class AudioEnhancementNet(nn.Module):
    def __init__(self, n_fft=2048, hop_length=512, n_mels=128):
        super(AudioEnhancementNet, self).__init__()
        self.n_fft = n_fft
        self.hop_length = hop_length
        self.n_mels = n_mels
        
        # 定义网络层
        self.conv1 = nn.Conv2d(1, 16, kernel_size=(3, 3), padding=1)
        self.bn1 = nn.BatchNorm2d(16)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=(3, 3), padding=1)
        self.bn2 = nn.BatchNorm2d(32)
        self.conv3 = nn.Conv2d(32, 16, kernel_size=(3, 3), padding=1)
        self.bn3 = nn.BatchNorm2d(16)
        self.conv4 = nn.Conv2d(16, 1, kernel_size=(3, 3), padding=1)
        
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()
    
    def forward(self, x):
        # x shape: (batch_size, 1, n_mels, time_frames)
        x = self.relu(self.bn1(self.conv1(x)))
        x = self.relu(self.bn2(self.conv2(x)))
        x = self.relu(self.bn3(self.conv3(x)))
        x = self.sigmoid(self.conv4(x))
        return x

class AudioQualityEnhancer:
    def __init__(self):
        print("初始化音频音质提升系统...")
        # 设置参数
        self.sample_rate = 22050
        self.n_fft = 2048
        self.hop_length = 512
        self.n_mels = 128
        
        # 创建增强网络
        self.model = AudioEnhancementNet(
            n_fft=self.n_fft,
            hop_length=self.hop_length,
            n_mels=self.n_mels
        )
        
        # 使用GPU（如果可用）
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)
        print(f"使用设备: {self.device}")
    
    def load_audio(self, audio_path):
        """加载音频文件"""
        try:
            audio, sr = librosa.load(audio_path, sr=self.sample_rate)
            # 确保音频是单声道
            if len(audio.shape) > 1:
                audio = np.mean(audio, axis=1)
            return audio, sr
        except Exception as e:
            print(f"无法加载音频文件: {e}")
            return None, None
    
    def save_audio(self, audio, sr, filename="enhanced_audio.wav"):
        """保存音频文件"""
        try:
            sf.write(filename, audio, sr)
            print(f"音频已保存到: {filename}")
            return filename
        except Exception as e:
            print(f"音频保存失败: {e}")
            return None
    
    def audio_to_mel(self, audio, sr):
        """将音频转换为梅尔谱图"""
        # 计算梅尔谱图
        S = librosa.feature.melspectrogram(
            y=audio,
            sr=sr,
            n_fft=self.n_fft,
            hop_length=self.hop_length,
            n_mels=self.n_mels
        )
        
        # 转换为分贝值
        S_dB = librosa.power_to_db(S, ref=np.max)
        
        # 归一化
        S_norm = (S_dB + 80) / 80  # 将范围从[-80, 0]映射到[0, 1]
        
        return S_norm
    
    def mel_to_audio(self, mel_spec, sr):
        """将梅尔谱图转换回音频"""
        # 反归一化
        mel_spec_db = mel_spec * 80 - 80
        
        # 转换为振幅
        S = librosa.db_to_power(mel_spec_db)
        
        # 使用Griffin-Lim算法重建音频
        audio = librosa.feature.inverse.mel_to_audio(
            S,
            sr=sr,
            n_fft=self.n_fft,
            hop_length=self.hop_length
        )
        
        return audio
    
    def enhance_audio(self, audio_path, output_path="enhanced_audio.wav", bass_boost=1.5, clarity_boost=1.2):
        """执行音频音质提升"""
        try:
            print(f"正在提升音频音质: {audio_path}")
            
            # 加载音频
            audio, sr = self.load_audio(audio_path)
            
            if audio is None:
                return None
            
            # 转换为梅尔谱图
            mel_spec = self.audio_to_mel(audio, sr)
            
            # 在梅尔谱图上应用增强（简化版）
            # 注意：在实际应用中，这里应该使用训练好的深度学习模型
            # 这里我们使用简单的频谱增强作为演示
            enhanced_mel = mel_spec.copy()
            
            # 低音增强（增强低频部分）
            low_freq_range = int(self.n_mels * 0.2)  # 前20%的频率范围
            enhanced_mel[:low_freq_range, :] = np.minimum(1.0, enhanced_mel[:low_freq_range, :] * bass_boost)
            
            # 清晰度增强（增强中频部分）
            mid_freq_start = int(self.n_mels * 0.2)
            mid_freq_end = int(self.n_mels * 0.6)
            enhanced_mel[mid_freq_start:mid_freq_end, :] = np.minimum(1.0, enhanced_mel[mid_freq_start:mid_freq_end, :] * clarity_boost)
            
            # 转换回音频
            enhanced_audio = self.mel_to_audio(enhanced_mel, sr)
            
            # 标准化音频电平
            max_val = np.max(np.abs(enhanced_audio))
            if max_val > 0:
                enhanced_audio = enhanced_audio / max_val * 0.9
            
            # 保存增强后的音频
            saved_file = self.save_audio(enhanced_audio, sr, output_path)
            
            # 可视化增强结果
            self.visualize_enhancement(audio, enhanced_audio, sr)
            
            return saved_file
        except Exception as e:
            print(f"音频音质提升失败: {e}")
            return None
    
    def visualize_enhancement(self, original_audio, enhanced_audio, sr):
        """可视化音质提升结果"""
        try:
            plt.figure(figsize=(16, 12))
            
            # 绘制原始音频波形
            plt.subplot(3, 2, 1)
            librosa.display.waveshow(original_audio, sr=sr)
            plt.title('原始音频波形')
            plt.xlabel('时间 (秒)')
            plt.ylabel('振幅')
            
            # 绘制增强后音频波形
            plt.subplot(3, 2, 2)
            librosa.display.waveshow(enhanced_audio, sr=sr)
            plt.title('增强后音频波形')
            plt.xlabel('时间 (秒)')
            plt.ylabel('振幅')
            
            # 绘制原始音频梅尔谱图
            plt.subplot(3, 2, 3)
            S_original = librosa.feature.melspectrogram(y=original_audio, sr=sr, n_mels=self.n_mels)
            S_dB_original = librosa.power_to_db(S_original, ref=np.max)
            librosa.display.specshow(S_dB_original, x_axis='time', y_axis='mel', sr=sr, fmax=8000)
            plt.colorbar(format='%+2.0f dB')
            plt.title('原始音频梅尔谱图')
            
            # 绘制增强后音频梅尔谱图
            plt.subplot(3, 2, 4)
            S_enhanced = librosa.feature.melspectrogram(y=enhanced_audio, sr=sr, n_mels=self.n_mels)
            S_dB_enhanced = librosa.power_to_db(S_enhanced, ref=np.max)
            librosa.display.specshow(S_dB_enhanced, x_axis='time', y_axis='mel', sr=sr, fmax=8000)
            plt.colorbar(format='%+2.0f dB')
            plt.title('增强后音频梅尔谱图')
            
            # 绘制频谱差异
            plt.subplot(3, 1, 3)
            freq_bins = librosa.mel_frequencies(n_mels=self.n_mels, fmax=8000)
            original_mean_spec = np.mean(S_dB_original, axis=1)
            enhanced_mean_spec = np.mean(S_dB_enhanced, axis=1)
            
            plt.plot(freq_bins/1000, original_mean_spec, label='原始音频')
            plt.plot(freq_bins/1000, enhanced_mean_spec, label='增强后音频')
            plt.title('频谱对比')
            plt.xlabel('频率 (kHz)')
            plt.ylabel('分贝 (dB)')
            plt.legend()
            plt.grid(True)
            
            # 添加增强指示标记
            plt.axvspan(0, 1, alpha=0.2, color='blue', label='低音增强区域')
            plt.axvspan(1, 3, alpha=0.2, color='green', label='清晰度增强区域')
            plt.legend()
            
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            print(f"音频可视化失败: {e}")
    
    def batch_enhance(self, audio_paths, output_dir="./enhanced_output", **kwargs):
        """批量提升音频音质"""
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        results = []
        
        for audio_path in audio_paths:
            if os.path.exists(audio_path):
                # 获取文件名
                filename = os.path.basename(audio_path)
                print(f"\n处理文件: {filename}")
                
                # 设置输出路径
                output_path = os.path.join(output_dir, f"enhanced_{filename}")
                
                # 执行音质提升
                saved_file = self.enhance_audio(audio_path, output_path, **kwargs)
                
                if saved_file:
                    results.append({
                        'input_file': audio_path,
                        'output_file': saved_file
                    })
            else:
                print(f"文件不存在: {audio_path}")
        
        print(f"\n批量音质提升完成，共处理 {len(results)} 个文件")
        return results

# 使用示例
if __name__ == "__main__":
    # 创建音频音质提升实例
    quality_enhancer = AudioQualityEnhancer()
    
    # 示例1：提升单个音频文件的音质
    print("\n=== 示例1：提升单个音频文件的音质 ===")
    
    # 音频文件路径
    audio_path = "low_quality_audio.wav"
    
    # 检查文件是否存在
    if os.path.exists(audio_path):
        # 执行音质提升
        # 可以调整参数: bass_boost（低音增强程度）和clarity_boost（清晰度增强程度）
        enhanced_file = quality_enhancer.enhance_audio(
            audio_path, 
            "enhanced_result.wav",
            bass_boost=1.5,  # 低音增强1.5倍
            clarity_boost=1.2  # 清晰度增强1.2倍
        )
        
        if enhanced_file:
            print(f"\n音质提升完成，结果已保存到: {enhanced_file}")
    else:
        print(f"文件不存在: {audio_path}")
        print("请提供有效的音频文件路径")
    
    # 示例2：批量提升音频音质
    print("\n=== 示例2：批量提升音频音质 ===")
    
    # 音频文件列表（需要替换为实际文件路径）
    audio_files = ["low_quality1.wav", "low_quality2.wav"]  # 示例文件
    valid_files = [f for f in audio_files if os.path.exists(f)]
    
    if valid_files:
        # 批量处理
        batch_results = quality_enhancer.batch_enhance(
            valid_files, 
            output_dir="enhanced_batch",
            bass_boost=1.4,
            clarity_boost=1.1
        )
    else:
        print("没有找到有效的音频文件进行批量处理")
    
    print("\n提示：这是一个简化版的音质提升示例。在实际应用中，建议使用训练好的深度学习模型，")
    print("如Wave-U-Net、Spleeter或其他专门的音频增强模型，以获得更好的音质提升效果。")
    print("\n音频音质提升处理完成！")
```

## 最佳实践

在使用AI音频增强技术时，以下是一些最佳实践建议：

### 1. 数据准备与预处理
- 收集多样化的训练数据，涵盖不同的噪声类型、音频质量和场景
- 对音频数据进行准确的标注，特别是噪声样本和干净样本的配对
- 进行数据增强，如添加不同类型和强度的噪声
- 对音频进行预处理，如归一化、分段、重采样等
- 合理划分训练集、验证集和测试集

### 2. 模型选择与训练
- 根据具体的增强任务（噪声消除、混音分离、音质提升等）选择合适的模型架构
- 考虑模型的计算复杂度和推理速度，特别是在资源受限的环境中
- 优先使用预训练模型并进行微调，以提高性能和减少训练时间
- 使用适当的损失函数，如波形域的L1/L2损失或频谱域的STFT损失
- 采用混合损失函数，结合时域和频域的损失

### 3. 特征工程
- 根据任务需求选择合适的音频特征表示方法
- 考虑使用梅尔谱图、语谱图等时频表示作为模型输入
- 对特征进行归一化处理，以提高模型的训练稳定性
- 考虑使用多尺度特征，同时捕捉音频的局部和全局信息
- 使用数据标准化和增强技术提高模型的泛化能力

### 4. 后处理技术
- 对增强后的音频进行电平标准化，避免音量过大或过小
- 应用动态范围压缩，改善音频的动态特性
- 使用低通滤波器去除可能的高频噪声和伪影
- 对音频进行平滑处理，减少突变和失真
- 根据应用场景进行特定的后处理优化

### 5. 质量评估与验证
- 使用客观评估指标，如信噪比（SNR）、分段信噪比（SSNR）、短时间客观可懂度（STOI）等
- 进行主观评估，通过人类听众评价音频质量
- 在不同的测试场景和设备上验证增强效果
- 分析增强算法在极端条件下的表现
- 建立基准系统，持续监控和改进增强效果

### 6. 部署与优化
- 根据部署环境选择合适的模型格式和推理引擎
- 考虑模型量化、剪枝等技术，提高推理速度和降低内存占用
- 实现高效的音频处理流水线，包括输入处理、模型推理和输出后处理
- 考虑使用边缘计算设备进行本地音频增强
- 建立实时监控系统，跟踪增强效果和系统性能

通过遵循这些最佳实践，你可以更有效地使用AI音频增强技术，开发出高性能、高质量的音频增强应用。