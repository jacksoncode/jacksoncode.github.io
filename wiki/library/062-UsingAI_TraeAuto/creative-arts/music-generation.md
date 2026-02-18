# 音乐生成

AI音乐生成是利用人工智能技术自动创作、编排和生成音乐作品的过程。随着深度学习和生成模型的快速发展，AI已经能够生成从简单旋律到复杂交响乐的各种类型音乐，为音乐创作领域带来了前所未有的可能性。本章将详细介绍AI音乐生成的基本原理、主要应用场景以及实用的使用示例，帮助你掌握如何利用AI进行音乐创作和制作。

## AI音乐生成的基本原理

AI音乐生成主要基于深度学习模型，特别是生成式对抗网络（GANs）、变分自编码器（VAEs）和最新的扩散模型。这些模型通过学习大量的音乐数据，掌握了音乐的结构、和声、节奏等特征，并能够生成具有类似特性的新音乐作品。

### 主要技术方法

- **生成式对抗网络（GANs）**：通过生成器和判别器的对抗训练生成音乐
- **变分自编码器（VAEs）**：学习音乐的潜在表示并生成新样本
- **Transformer模型**：利用自注意力机制捕获长距离的音乐依赖关系
- **扩散模型**：通过迭代降噪过程生成高质量音乐
- **神经符号系统**：结合符号推理和神经网络生成结构化音乐

### 核心技术原理

#### 音乐生成的工作原理
1. **数据准备**：将原始音乐数据转换为模型可处理的格式
2. **模型训练**：使用大量音乐数据训练生成模型
3. **条件控制**：提供风格、情绪、速度等条件来引导生成过程
4. **音乐生成**：根据输入条件生成新的音乐内容
5. **后处理**：对生成的音乐进行优化和调整
6. **格式转换**：将生成的音乐转换为标准音频格式

#### 常用的音乐生成模型

- **MuseNet**：OpenAI开发的能够生成多种乐器和风格的音乐生成模型
- **MusicLM**：Google开发的能够根据文本描述生成音乐的模型
- **Jukebox**：OpenAI开发的能够生成特定艺术家风格的音乐模型
- **AudioCraft**：Meta开发的音频生成平台，包含音乐生成模型
- **MusicGen**：基于Transformer架构的音乐生成模型
- **Amper Music**：商业音乐生成平台，提供多种音乐生成工具
- **AIVA**：专注于古典音乐创作的AI系统
- **Soundraw**：提供定制音乐生成服务的平台

## AI音乐生成的应用场景

AI音乐生成技术已经在多个领域得到广泛应用，以下是一些常见的应用场景：

### 1. 原创音乐创作
- 辅助作曲家创作新作品
- 生成完整的音乐作品
- 提供灵感和创意起点
- 探索新的音乐风格和可能性
- 自动完成未完成的音乐片段

### 2. 内容创作配乐
- 为视频内容生成背景音乐
- 为游戏开发定制游戏音乐
- 为广告和营销内容创作配乐
- 为播客和有声读物添加背景音乐
- 为社交媒体内容生成定制音乐

### 3. 音乐教育
- 为音乐学习者提供示例曲目
- 生成特定风格和技巧的练习材料
- 辅助音乐理论教学
- 分析和解释音乐结构
- 模拟不同演奏风格和技巧

### 4. 个性化音乐服务
- 为用户生成个性化的音乐推荐
- 基于用户情绪和活动生成适配的音乐
- 创建个性化的冥想和放松音乐
- 生成适合不同场景的背景音乐
- 为健身和运动生成节奏匹配的音乐

### 5. 音乐制作和编曲
- 自动为旋律创建和声伴奏
- 为歌曲生成不同风格的编曲版本
- 智能混音和母带处理
- 生成鼓点和节奏部分
- 自动化音乐制作工作流程

### 6. 音乐产业应用
- 音乐版权库扩充
- 快速原型制作
- 降低音乐制作成本
- 为独立艺术家提供创作工具
- 音乐风格分析和预测

### 7. 实验性音乐探索
- 融合不同音乐风格的实验
- 探索人类难以创作的复杂音乐结构
- 生成基于科学数据或自然现象的音乐
- 跨艺术形式的音乐表达
- 开发新型音乐交互界面

### 8. 辅助残障音乐人
- 为身体受限的音乐人提供创作工具
- 语音控制的音乐创作系统
- 简化复杂的音乐制作流程
- 提供替代性的音乐表达方式
- 增强音乐创作的可访问性

## 基础音乐生成示例

下面是一个使用Python和常用的音乐生成库进行基础音乐生成的实现示例：

```python
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import pretty_midi
import openai

class AIMusicGenerator:
    def __init__(self, api_key=None):
        # 初始化OpenAI API
        if api_key:
            openai.api_key = api_key
        elif 'OPENAI_API_KEY' in os.environ:
            openai.api_key = os.environ['OPENAI_API_KEY']
        else:
            print("警告：未提供OpenAI API密钥，某些功能可能无法使用")
            self.openai_available = False
            return
        
        self.openai_available = True
        self.model = "gpt-4o"
        self.temperature = 0.7
        
        # 设置输出目录
        self.output_dir = "output_music"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
    def generate_music_with_text_prompt(self, prompt, duration=30, format="midi", genre=None, tempo=None):
        """
        使用文本提示生成音乐
        prompt: 描述想要生成的音乐特征的文本
        duration: 音乐时长（秒）
        format: 输出格式（midi或audio）
        genre: 音乐类型
        tempo: 速度（BPM）
        """
        if not self.openai_available:
            print("错误：需要OpenAI API密钥才能使用此功能")
            return None
        
        try:
            # 构建提示词
            full_prompt = f"""\请生成一段音乐，满足以下要求：
            
            描述：{prompt}
            
            {f'音乐类型：{genre}\n' if genre else ''}
            {f'速度（BPM）：{tempo}\n' if tempo else ''}
            时长：约{duration}秒
            
            请以MIDI格式返回音乐，使用标准的MIDI事件表示法，不包含任何额外的解释或说明。
            """
            
            # 调用OpenAI API
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一位专业的音乐作曲家，擅长根据文本描述创作音乐。"},
                    {"role": "user", "content": full_prompt}
                ],
                temperature=self.temperature,
                max_tokens=2000
            )
            
            # 提取MIDI内容
            midi_content = response['choices'][0]['message']['content']
            
            # 保存MIDI文件
            output_file = os.path.join(self.output_dir, f"generated_music_{int(time.time())}.mid")
            
            # 解析MIDI内容并保存（这里简化处理，实际项目中需要更复杂的解析）
            with open(output_file, "w") as f:
                f.write(midi_content)
            
            print(f"音乐已生成并保存到：{output_file}")
            
            # 如果需要音频格式，可以使用其他库转换
            if format == "audio":
                # 这里简化处理，实际项目中需要使用MIDI转音频的库
                print("提示：MIDI转音频功能需要额外的音频合成库支持")
                
            return output_file
            
        except Exception as e:
            print(f"生成音乐时发生错误: {str(e)}")
            return None
        
    def generate_simple_melody(self, key="C", scale="major", length=16, tempo=120):
        """
        生成简单的旋律（不依赖OpenAI API）
        key: 调号（如"C", "D", "E"等）
        scale: 音阶类型（"major"或"minor"）
        length: 旋律长度（小节数）
        tempo: 速度（BPM）
        """
        try:
            # 创建一个PrettyMIDI对象
            midi = pretty_midi.PrettyMIDI(initial_tempo=tempo)
            
            # 创建一个钢琴乐器
            piano = pretty_midi.Instrument(program=0)  # 0表示钢琴
            
            # 定义音阶音符
            note_names = {}
            if scale == "major":
                # 大调音阶的音程（全音、全音、半音、全音、全音、全音、半音）
                intervals = [0, 2, 4, 5, 7, 9, 11]
            else:  # minor
                # 小调音阶的音程（全音、半音、全音、全音、半音、全音、全音）
                intervals = [0, 2, 3, 5, 7, 8, 10]
            
            # 构建音符名称列表
            base_note = pretty_midi.note_name_to_number(f"{key}4")
            scale_notes = [base_note + interval for interval in intervals]
            
            # 生成随机旋律
            beats_per_measure = 4  # 4/4拍
            total_beats = length * beats_per_measure
            
            # 随机选择音符长度分布
            note_lengths = [0.25, 0.5, 1.0, 2.0]  # 四分音符、八分音符等
            note_probs = [0.4, 0.3, 0.2, 0.1]  # 对应长度的概率
            
            # 当前时间位置
            current_time = 0
            
            while current_time < total_beats:
                # 随机选择音符长度
                note_length = np.random.choice(note_lengths, p=note_probs)
                
                # 确保音符不会超出总时长
                if current_time + note_length > total_beats:
                    note_length = total_beats - current_time
                
                # 随机选择一个音阶中的音符
                note_number = np.random.choice(scale_notes)
                
                # 随机调整音高（上下一个八度）
                octave_shift = np.random.choice([-12, 0, 12], p=[0.2, 0.6, 0.2])
                note_number += octave_shift
                
                # 确保音符在合理范围内
                note_number = max(21, min(108, note_number))  # 钢琴的音域
                
                # 创建音符
                note = pretty_midi.Note(
                    velocity=np.random.randint(60, 100),  # 力度
                    pitch=note_number,
                    start=current_time,
                    end=current_time + note_length
                )
                
                # 添加到钢琴轨道
                piano.notes.append(note)
                
                # 更新当前时间
                current_time += note_length
            
            # 添加钢琴到MIDI对象
            midi.instruments.append(piano)
            
            # 保存MIDI文件
            output_file = os.path.join(self.output_dir, f"simple_melody_{key}_{scale}_{int(time.time())}.mid")
            midi.write(output_file)
            
            print(f"简单旋律已生成并保存到：{output_file}")
            return output_file
            
        except Exception as e:
            print(f"生成简单旋律时发生错误: {str(e)}")
            return None
        
    def generate_chord_progression(self, key="C", progression=[1, 4, 5, 1], length=4, tempo=120):
        """
        生成和弦进行
        key: 调号
        progression: 和弦级数进行（罗马数字表示）
        length: 每个和弦持续的小节数
        tempo: 速度（BPM）
        """
        try:
            # 创建一个PrettyMIDI对象
            midi = pretty_midi.PrettyMIDI(initial_tempo=tempo)
            
            # 创建一个钢琴乐器
            piano = pretty_midi.Instrument(program=0)  # 钢琴
            
            # 定义和弦结构（大调和弦的三和弦）
            chord_structures = {
                1: [0, 4, 7],     # 大三和弦
                2: [0, 4, 7],     # 大三和弦
                3: [0, 3, 7],     # 小三和弦
                4: [0, 4, 7],     # 大三和弦
                5: [0, 4, 7],     # 大三和弦
                6: [0, 3, 7],     # 小三和弦
                7: [0, 3, 6]      # 减三和弦
            }
            
            # 获取调号的基础音符
            base_note = pretty_midi.note_name_to_number(f"{key}3")
            
            # 定义大调音阶的音程
            major_scale_intervals = [0, 2, 4, 5, 7, 9, 11]
            
            # 生成和弦进行
            current_time = 0
            beats_per_measure = 4  # 4/4拍
            beats_per_chord = length * beats_per_measure
            
            for chord_degree in progression:
                # 获取和弦根音在音阶中的位置
                root_index = (chord_degree - 1) % 7
                root_note = base_note + major_scale_intervals[root_index]
                
                # 获取和弦结构
                chord_notes = chord_structures.get(chord_degree, [0, 4, 7])
                
                # 生成和弦音符（包含低八度和高八度）
                for octave_offset in [-12, 0, 12]:
                    for interval in chord_notes:
                        note_number = root_note + interval + octave_offset
                        
                        # 确保音符在合理范围内
                        if 21 <= note_number <= 108:
                            note = pretty_midi.Note(
                                velocity=80,  # 固定力度
                                pitch=note_number,
                                start=current_time,
                                end=current_time + beats_per_chord
                            )
                            piano.notes.append(note)
                
                # 更新当前时间
                current_time += beats_per_chord
            
            # 添加钢琴到MIDI对象
            midi.instruments.append(piano)
            
            # 保存MIDI文件
            output_file = os.path.join(self.output_dir, f"chord_progression_{key}_{'_'.join(map(str, progression))}_{int(time.time())}.mid")
            midi.write(output_file)
            
            print(f"和弦进行已生成并保存到：{output_file}")
            return output_file
            
        except Exception as e:
            print(f"生成和弦进行时发生错误: {str(e)}")
            return None
        
    def generate_drum_pattern(self, style="pop", length=4, tempo=120):
        """
        生成鼓点节奏
        style: 鼓点风格
        length: 长度（小节数）
        tempo: 速度（BPM）
        """
        try:
            # 创建一个PrettyMIDI对象
            midi = pretty_midi.PrettyMIDI(initial_tempo=tempo)
            
            # 创建一个鼓组乐器
            drums = pretty_midi.Instrument(program=0, is_drum=True)
            
            # 定义不同鼓的MIDI音符号
            drum_notes = {
                'kick': 36,          # 底鼓
                'snare': 38,         # 军鼓
                'hihat_closed': 42,  # 闭镲
                'hihat_open': 46,    # 开镲
                'ride': 51,          # 节奏镲
                'crash': 49          # 吊镲
            }
            
            # 定义不同风格的鼓点模式
            patterns = {
                'pop': {
                    'kick': [1, 0, 0, 0, 1, 0, 0, 0],          # 每小节第1和第5拍
                    'snare': [0, 0, 0, 0, 1, 0, 0, 0],         # 每小节第5拍
                    'hihat_closed': [1, 1, 1, 1, 1, 1, 1, 1]   # 每八拍都有
                },
                'rock': {
                    'kick': [1, 0, 0, 0, 1, 0, 0, 0],
                    'snare': [0, 0, 0, 0, 1, 0, 0, 0],
                    'hihat_closed': [1, 0, 1, 0, 1, 0, 1, 0],
                    'ride': [1, 1, 1, 1, 1, 1, 1, 1]
                },
                'jazz': {
                    'kick': [1, 0, 0, 0, 0, 0, 0, 0],
                    'snare': [0, 0, 1, 0, 0, 0, 1, 0],
                    'hihat_closed': [1, 1, 1, 1, 1, 1, 1, 1]
                }
            }
            
            # 获取选择的风格模式
            pattern = patterns.get(style, patterns['pop'])
            
            # 生成鼓点
            beats_per_measure = 4  # 4/4拍
            beat_duration = 60.0 / tempo  # 每拍的时长（秒）
            step_duration = beat_duration / 2  # 八分音符时长
            
            for measure in range(length):
                for step in range(len(pattern.get('hihat_closed', []))):
                    current_time = (measure * beats_per_measure * 2 + step) * step_duration
                    
                    # 添加底鼓
                    if 'kick' in pattern and pattern['kick'][step % len(pattern['kick'])]:
                        note = pretty_midi.Note(
                            velocity=90,
                            pitch=drum_notes['kick'],
                            start=current_time,
                            end=current_time + step_duration * 0.7
                        )
                        drums.notes.append(note)
                    
                    # 添加军鼓
                    if 'snare' in pattern and pattern['snare'][step % len(pattern['snare'])]:
                        note = pretty_midi.Note(
                            velocity=85,
                            pitch=drum_notes['snare'],
                            start=current_time,
                            end=current_time + step_duration * 0.7
                        )
                        drums.notes.append(note)
                    
                    # 添加闭镲
                    if 'hihat_closed' in pattern and pattern['hihat_closed'][step]:
                        note = pretty_midi.Note(
                            velocity=70,
                            pitch=drum_notes['hihat_closed'],
                            start=current_time,
                            end=current_time + step_duration * 0.3
                        )
                        drums.notes.append(note)
                    
                    # 添加开镲或节奏镲
                    if 'hihat_open' in pattern and pattern['hihat_open'][step % len(pattern['hihat_open'])]:
                        note = pretty_midi.Note(
                            velocity=75,
                            pitch=drum_notes['hihat_open'],
                            start=current_time,
                            end=current_time + step_duration * 0.8
                        )
                        drums.notes.append(note)
                    
                    if 'ride' in pattern and pattern['ride'][step % len(pattern['ride'])]:
                        note = pretty_midi.Note(
                            velocity=65,
                            pitch=drum_notes['ride'],
                            start=current_time,
                            end=current_time + step_duration * 0.8
                        )
                        drums.notes.append(note)
            
            # 添加鼓组到MIDI对象
            midi.instruments.append(drums)
            
            # 保存MIDI文件
            output_file = os.path.join(self.output_dir, f"drum_pattern_{style}_{length}bars_{int(time.time())}.mid")
            midi.write(output_file)
            
            print(f"鼓点节奏已生成并保存到：{output_file}")
            return output_file
            
        except Exception as e:
            print(f"生成鼓点节奏时发生错误: {str(e)}")
            return None
        
    def create_song_structure(self, genre="pop", sections=None):
        """
        创建完整的歌曲结构
        genre: 音乐类型
        sections: 歌曲段落定义
        """
        try:
            if sections is None:
                # 默认流行歌曲结构
                sections = [
                    {"name": "intro", "length": 4, " instruments": ["melody", "chords"]},
                    {"name": "verse", "length": 8, " instruments": ["melody", "chords", "drums"]},
                    {"name": "pre-chorus", "length": 4, " instruments": ["melody", "chords", "drums"]},
                    {"name": "chorus", "length": 8, " instruments": ["melody", "chords", "drums"]},
                    {"name": "verse2", "length": 8, " instruments": ["melody", "chords", "drums"]},
                    {"name": "pre-chorus2", "length": 4, " instruments": ["melody", "chords", "drums"]},
                    {"name": "chorus2", "length": 8, " instruments": ["melody", "chords", "drums"]},
                    {"name": "bridge", "length": 8, " instruments": ["melody", "chords", "drums"]},
                    {"name": "chorus3", "length": 12, " instruments": ["melody", "chords", "drums"]},
                    {"name": "outro", "length": 4, " instruments": ["melody", "chords"]}
                ]
            
            print(f"创建{genre}风格的歌曲结构，包含{len(sections)}个段落")
            
            # 在实际项目中，这里会生成每个段落的音乐并组合起来
            # 这里仅作为示例，输出结构信息
            for i, section in enumerate(sections):
                print(f"段落{i+1}: {section['name']} ({section['length']}小节) - 乐器: {', '.join(section[' instruments'])}")
            
            print("提示：完整歌曲生成功能需要将各段落音乐生成并组合")
            return sections
            
        except Exception as e:
            print(f"创建歌曲结构时发生错误: {str(e)}")
            return None

# 使用示例
if __name__ == "__main__":
    # 导入必要的库
    import time
    
    try:
        # 初始化AI音乐生成器
        music_generator = AIMusicGenerator()
        
        # 示例1: 生成简单旋律
        print("\n=== 示例1: 生成简单旋律 ===")
        melody_file = music_generator.generate_simple_melody(key="C", scale="major", length=8, tempo=120)
        
        # 示例2: 生成和弦进行
        print("\n=== 示例2: 生成和弦进行 ===")
        chord_file = music_generator.generate_chord_progression(key="C", progression=[1, 4, 5, 1], length=2, tempo=120)
        
        # 示例3: 生成鼓点节奏
        print("\n=== 示例3: 生成鼓点节奏 ===")
        drum_file = music_generator.generate_drum_pattern(style="pop", length=4, tempo=120)
        
        # 示例4: 创建歌曲结构
        print("\n=== 示例4: 创建歌曲结构 ===")
        song_structure = music_generator.create_song_structure(genre="pop")
        
        # 示例5: 使用OpenAI API生成音乐（需要API密钥）
        if music_generator.openai_available:
            print("\n=== 示例5: 使用OpenAI API生成音乐 ===")
            # 注意：实际运行时需要有效的OpenAI API密钥
            # music_file = music_generator.generate_music_with_text_prompt(
            #     prompt="一段欢快的钢琴旋律，适合作为视频背景音乐",
            #     duration=30,
            #     genre="钢琴独奏",
            #     tempo=100
            # )
            print("提示：OpenAI API音乐生成功能已配置，但在示例中未实际调用以避免API费用")
            
    except ImportError as e:
        print(f"缺少必要的库: {str(e)}")
        print("请安装所需依赖: pip install numpy matplotlib pretty_midi openai")
        
    except Exception as e:
        print(f"程序运行出错: {str(e)}")
        
    print("\n提示：")
    print("1. 确保已安装所需依赖: pip install numpy matplotlib pretty_midi openai")
    print("2. 生成的MIDI文件可以用音乐软件打开和编辑，如GarageBand、Logic Pro、Ableton Live等")
    print("3. 若要转换为音频文件，可以使用MIDI合成器或在线转换工具")
    print("4. 使用OpenAI API时，确保设置了有效的API密钥")
    print("5. 调整参数可以生成不同风格和长度的音乐")
```

## 高级音乐生成功能

除了基础的音乐生成功能，AI还可以实现更高级的音乐生成功能，如风格迁移、歌词与音乐同步生成等。下面是一个高级音乐生成的示例：

```python
import os
import numpy as np
import pretty_midi
import openai
import librosa
import soundfile as sf

class AdvancedAIMusicGenerator:
    def __init__(self, api_key=None):
        # 初始化OpenAI API
        if api_key:
            openai.api_key = api_key
        elif 'OPENAI_API_KEY' in os.environ:
            openai.api_key = os.environ['OPENAI_API_KEY']
        else:
            print("警告：未提供OpenAI API密钥，某些高级功能可能无法使用")
            self.openai_available = False
            return
        
        self.openai_available = True
        self.model = "gpt-4o"
        self.temperature = 0.7
        
        # 设置输出目录
        self.output_dir = "advanced_output_music"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
    def music_style_transfer(self, original_music, target_style, duration=None):
        """
        音乐风格迁移
        original_music: 原始音乐描述或MIDI文件路径
        target_style: 目标音乐风格
        duration: 时长（秒）
        """
        if not self.openai_available:
            print("错误：需要OpenAI API密钥才能使用此功能")
            return None
        
        try:
            # 构建提示词
            full_prompt = f"""\请将以下音乐转换为{target_style}风格：
            
            原始音乐：{original_music}
            
            {f'时长：约{duration}秒\n' if duration else ''}
            
            请保留原始音乐的基本旋律和结构，但完全改变其风格以匹配目标风格。
            
            请以MIDI格式返回转换后的音乐，使用标准的MIDI事件表示法，不包含任何额外的解释或说明。
            """
            
            # 调用OpenAI API
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一位精通多种音乐风格的作曲家，擅长音乐风格转换。"},
                    {"role": "user", "content": full_prompt}
                ],
                temperature=self.temperature,
                max_tokens=3000
            )
            
            # 提取MIDI内容
            midi_content = response['choices'][0]['message']['content']
            
            # 保存MIDI文件
            output_file = os.path.join(self.output_dir, f"style_transfer_{target_style}_{int(time.time())}.mid")
            
            # 解析MIDI内容并保存
            with open(output_file, "w") as f:
                f.write(midi_content)
            
            print(f"风格转换后的音乐已生成并保存到：{output_file}")
            return output_file
            
        except Exception as e:
            print(f"进行音乐风格迁移时发生错误: {str(e)}")
            return None
        
    def generate_music_from_lyrics(self, lyrics, genre=None, tempo=None):
        """
        根据歌词生成音乐
        lyrics: 歌词文本
        genre: 音乐类型
        tempo: 速度（BPM）
        """
        if not self.openai_available:
            print("错误：需要OpenAI API密钥才能使用此功能")
            return None
        
        try:
            # 构建提示词
            full_prompt = f"""\请根据以下歌词创作一段音乐：
            
            歌词：
            {lyrics}
            
            {f'音乐类型：{genre}\n' if genre else ''}
            {f'速度（BPM）：{tempo}\n' if tempo else ''}
            
            请创作与歌词情绪和内容相匹配的旋律和和声，确保音乐节奏与歌词的韵律相协调。
            
            请以MIDI格式返回创作的音乐，使用标准的MIDI事件表示法，并包含歌词与音符的对应关系。
            不包含任何额外的解释或说明。
            """
            
            # 调用OpenAI API
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一位专业的词曲作者，擅长根据歌词创作匹配的音乐。"},
                    {"role": "user", "content": full_prompt}
                ],
                temperature=self.temperature,
                max_tokens=3000
            )
            
            # 提取MIDI内容
            midi_content = response['choices'][0]['message']['content']
            
            # 保存MIDI文件
            output_file = os.path.join(self.output_dir, f"music_from_lyrics_{int(time.time())}.mid")
            
            # 解析MIDI内容并保存
            with open(output_file, "w") as f:
                f.write(midi_content)
            
            print(f"根据歌词生成的音乐已保存到：{output_file}")
            return output_file
            
        except Exception as e:
            print(f"根据歌词生成音乐时发生错误: {str(e)}")
            return None
        
    def generate_music_with_emotion(self, emotion, genre=None, tempo=None, duration=30):
        """
        根据情绪生成音乐
        emotion: 情绪描述
        genre: 音乐类型
        tempo: 速度（BPM）
        duration: 时长（秒）
        """
        if not self.openai_available:
            print("错误：需要OpenAI API密钥才能使用此功能")
            return None
        
        try:
            # 构建提示词
            full_prompt = f"""\请创作一段能够表达{emotion}情绪的音乐：
            
            {f'音乐类型：{genre}\n' if genre else ''}
            {f'速度（BPM）：{tempo}\n' if tempo else ''}
            时长：约{duration}秒
            
            请确保音乐的旋律、和声、节奏和乐器选择都能够有效传达指定的情绪。
            
            请以MIDI格式返回创作的音乐，使用标准的MIDI事件表示法，不包含任何额外的解释或说明。
            """
            
            # 调用OpenAI API
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一位擅长情感表达的作曲家，能够创作准确传达特定情绪的音乐。"},
                    {"role": "user", "content": full_prompt}
                ],
                temperature=self.temperature,
                max_tokens=3000
            )
            
            # 提取MIDI内容
            midi_content = response['choices'][0]['message']['content']
            
            # 保存MIDI文件
            output_file = os.path.join(self.output_dir, f"emotional_music_{emotion}_{int(time.time())}.mid")
            
            # 解析MIDI内容并保存
            with open(output_file, "w") as f:
                f.write(midi_content)
            
            print(f"表达{emotion}情绪的音乐已生成并保存到：{output_file}")
            return output_file
            
        except Exception as e:
            print(f"生成情感音乐时发生错误: {str(e)}")
            return None
        
    def generate_multi_track_music(self, genre, tracks=None, duration=60):
        """
        生成多轨音乐
        genre: 音乐类型
        tracks: 音轨定义
        duration: 时长（秒）
        """
        if not self.openai_available:
            print("错误：需要OpenAI API密钥才能使用此功能")
            return None
        
        try:
            if tracks is None:
                # 默认多轨配置
                tracks = [
                    {"name": "lead melody", "instrument": "piano", "description": "主要旋律线"},
                    {"name": "accompaniment", "instrument": "guitar", "description": "和弦伴奏"},
                    {"name": "bass", "instrument": "bass guitar", "description": "低音声部"},
                    {"name": "drums", "instrument": "drum kit", "description": "鼓点节奏"}
                ]
            
            # 格式化音轨信息
            tracks_info = "\n".join([f"- {track['name']} ({track['instrument']}): {track['description']}" for track in tracks])
            
            # 构建提示词
            full_prompt = f"""\请创作一段{genre}风格的多轨音乐：
            
            音轨配置：
            {tracks_info}
            
            时长：约{duration}秒
            
            请确保各音轨之间的和谐配合，创造出完整且专业的音乐作品。
            
            请以MIDI格式返回创作的音乐，使用标准的MIDI事件表示法，为每个音轨分配不同的通道。
            不包含任何额外的解释或说明。
            """
            
            # 调用OpenAI API
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一位专业的音乐制作人，擅长创作多轨音乐作品。"},
                    {"role": "user", "content": full_prompt}
                ],
                temperature=self.temperature,
                max_tokens=4000
            )
            
            # 提取MIDI内容
            midi_content = response['choices'][0]['message']['content']
            
            # 保存MIDI文件
            output_file = os.path.join(self.output_dir, f"multi_track_{genre}_{int(time.time())}.mid")
            
            # 解析MIDI内容并保存
            with open(output_file, "w") as f:
                f.write(midi_content)
            
            print(f"多轨{genre}音乐已生成并保存到：{output_file}")
            return output_file
            
        except Exception as e:
            print(f"生成多轨音乐时发生错误: {str(e)}")
            return None
        
    def generate_music_from_audio(self, audio_description, genre=None, tempo=None, duration=30):
        """
        根据音频描述生成音乐
        audio_description: 音频特征描述
        genre: 音乐类型
        tempo: 速度（BPM）
        duration: 时长（秒）
        """
        if not self.openai_available:
            print("错误：需要OpenAI API密钥才能使用此功能")
            return None
        
        try:
            # 构建提示词
            full_prompt = f"""\请根据以下音频特征描述创作音乐：
            
            音频特征描述：
            {audio_description}
            
            {f'音乐类型：{genre}\n' if genre else ''}
            {f'速度（BPM）：{tempo}\n' if tempo else ''}
            时长：约{duration}秒
            
            请创作符合描述的音乐，注意细节如音色、动态范围、空间感等。
            
            请以MIDI格式返回创作的音乐，使用标准的MIDI事件表示法，不包含任何额外的解释或说明。
            """
            
            # 调用OpenAI API
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一位音效设计师，擅长根据音频特征描述创作音乐。"},
                    {"role": "user", "content": full_prompt}
                ],
                temperature=self.temperature,
                max_tokens=3000
            )
            
            # 提取MIDI内容
            midi_content = response['choices'][0]['message']['content']
            
            # 保存MIDI文件
            output_file = os.path.join(self.output_dir, f"music_from_audio_desc_{int(time.time())}.mid")
            
            # 解析MIDI内容并保存
            with open(output_file, "w") as f:
                f.write(midi_content)
            
            print(f"根据音频描述生成的音乐已保存到：{output_file}")
            return output_file
            
        except Exception as e:
            print(f"根据音频描述生成音乐时发生错误: {str(e)}")
            return None

# 使用示例
if __name__ == "__main__":
    # 导入必要的库
    import time
    
    try:
        # 初始化高级AI音乐生成器
        advanced_music_generator = AdvancedAIMusicGenerator()
        
        if advanced_music_generator.openai_available:
            # 示例1: 音乐风格迁移
            print("\n=== 示例1: 音乐风格迁移 ===")
            original_music = "一段简单的C大调钢琴旋律，4/4拍，120 BPM"
            target_style = "爵士乐"
            # 注意：实际运行时需要有效的OpenAI API密钥
            # style_transfer_file = advanced_music_generator.music_style_transfer(
            #     original_music=original_music,
            #     target_style=target_style,
            #     duration=30
            # )
            print("提示：音乐风格迁移功能已配置，但在示例中未实际调用以避免API费用")
            
            # 示例2: 根据歌词生成音乐
            print("\n=== 示例2: 根据歌词生成音乐 ===")
            lyrics = """
            阳光照在我的脸上
            微风吹过发梢
            我想要自由地奔跑
            在这广阔的天地间
            
            鸟儿在枝头歌唱
            花儿在绽放微笑
            世界如此美好
            我心充满希望
            """
            # music_from_lyrics_file = advanced_music_generator.generate_music_from_lyrics(
            #     lyrics=lyrics,
            #     genre="流行",
            #     tempo=90
            # )
            print("提示：根据歌词生成音乐功能已配置，但在示例中未实际调用以避免API费用")
            
            # 示例3: 根据情绪生成音乐
            print("\n=== 示例3: 根据情绪生成音乐 ===")
            emotion = "平静和放松"
            # emotional_music_file = advanced_music_generator.generate_music_with_emotion(
            #     emotion=emotion,
            #     genre="新世纪音乐",
            #     tempo=60,
            #     duration=60
            # )
            print("提示：根据情绪生成音乐功能已配置，但在示例中未实际调用以避免API费用")
            
            # 示例4: 生成多轨音乐
            print("\n=== 示例4: 生成多轨音乐 ===")
            genre = "流行摇滚"
            custom_tracks = [
                {"name": "主唱旋律", "instrument": "lead vocal", "description": "主旋律声部"},
                {"name": "吉他伴奏", "instrument": "acoustic guitar", "description": "节奏吉他"},
                {"name": "主音吉他", "instrument": "electric guitar", "description": "solo吉他"},
                {"name": "贝斯", "instrument": "bass guitar", "description": "低音声部"},
                {"name": "鼓", "instrument": "drum kit", "description": "鼓点节奏"}
            ]
            # multi_track_file = advanced_music_generator.generate_multi_track_music(
            #     genre=genre,
            #     tracks=custom_tracks,
            #     duration=60
            # )
            print("提示：多轨音乐生成功能已配置，但在示例中未实际调用以避免API费用")
            
            # 示例5: 根据音频描述生成音乐
            print("\n=== 示例5: 根据音频描述生成音乐 ===")
            audio_description = """
            - 音色：温暖的钢琴，带有轻微的混响
            - 动态范围：中等，没有极端的音量变化
            - 节奏：平滑的三连音节奏
            - 旋律：缓慢上升的琶音
            - 和声：简单的三和弦进行
            - 空间感：适度的立体声宽度，轻微的延迟效果
            """
            # music_from_audio_file = advanced_music_generator.generate_music_from_audio(
            #     audio_description=audio_description,
            #     genre="古典",
            #     tempo=80,
            #     duration=45
            # )
            print("提示：根据音频描述生成音乐功能已配置，但在示例中未实际调用以避免API费用")
            
        else:
            print("警告：未提供OpenAI API密钥，无法使用高级音乐生成功能")
            
    except ImportError as e:
        print(f"缺少必要的库: {str(e)}")
        print("请安装所需依赖: pip install numpy pretty_midi openai librosa soundfile")
        
    except Exception as e:
        print(f"程序运行出错: {str(e)}")
        
    print("\n提示：")
    print("1. 确保已安装所需依赖: pip install numpy pretty_midi openai librosa soundfile")
    print("2. 高级音乐生成功能需要有效的OpenAI API密钥")
    print("3. 为获得最佳效果，提供详细的描述和上下文信息")
    print("4. 生成的MIDI文件可以导入到专业音乐制作软件中进一步编辑")
    print("5. 调整参数可以生成不同风格和情绪的音乐作品")
```

## 最佳实践

使用AI进行音乐生成时，以下是一些最佳实践：

### 1. 明确创作目标
- 确定音乐的用途和目标受众
- 明确音乐风格、情绪和长度要求
- 考虑音乐的结构和曲式
- 确定所需的乐器和音色

### 2. 提供详细的提示
- 使用具体、详细的描述语言
- 包含音乐理论术语以提高准确性
- 提供参考曲目或风格示例
- 明确说明偏好和限制条件

### 3. 迭代优化
- 从小规模的音乐片段开始
- 根据生成结果逐步调整提示词
- 对生成的音乐进行分段优化
- 组合多个生成结果创建完整作品

### 4. 结合人工创作
- 将AI生成作为创意起点而非终点
- 对生成的音乐进行人工编辑和调整
- 添加个人创意和风格元素
- 确保作品具有独特性和原创性

### 5. 学习音乐理论
- 了解基本的音乐理论知识
- 熟悉常见的音乐结构和曲式
- 掌握基本的和声学和旋律创作技巧
- 学习不同音乐风格的特点和元素

### 6. 使用专业工具
- 将AI生成的MIDI文件导入专业音乐软件
- 使用虚拟乐器和效果器增强音乐质量
- 应用混音和母带处理技术
- 利用音频编辑工具完善细节

### 7. 版权和伦理考虑
- 了解AI生成音乐的版权归属问题
- 确保不侵犯他人的知识产权
- 注明AI在创作过程中的作用
- 尊重音乐创作的伦理和道德准则

### 8. 持续学习和实践
- 尝试不同的AI音乐生成工具和模型
- 学习其他音乐人的创作技巧和方法
- 分析和研究成功的音乐作品
- 定期练习和实验新的创作方法

## 总结

AI音乐生成技术正在为音乐创作领域带来革命性的变化，为作曲家、音乐制作人和爱好者提供了强大的创作工具和灵感来源。从简单的旋律生成到复杂的多轨音乐创作，AI已经能够支持音乐创作的各个环节，帮助创作者探索新的音乐可能性。

随着深度学习和生成模型的不断进步，未来的AI音乐生成技术将更加智能、灵活和专业，能够更好地理解和实现创作者的意图，生成更高质量、更具表现力的音乐作品。对于音乐创作者来说，掌握AI音乐生成技术将成为提升创作效率和拓展创作领域的重要技能。

然而，我们也应该认识到，AI音乐生成技术是辅助创作的工具，而非替代人类创作的手段。真正优秀的音乐作品仍然需要人类的情感表达、创意构思和艺术判断。通过将AI技术与人类创造力相结合，我们可以开拓音乐创作的新边界，创造出更加丰富多彩的音乐作品。

无论是专业音乐人还是音乐爱好者，都可以利用AI音乐生成技术来激发创意、提高效率、探索新的音乐风格和可能性。随着技术的不断发展和普及，AI音乐生成将成为音乐创作领域不可或缺的一部分，为音乐世界带来更多惊喜和创新。