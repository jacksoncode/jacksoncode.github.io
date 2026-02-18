# 艺术创作

AI艺术创作是利用人工智能技术生成、辅助或增强视觉艺术作品的过程。随着生成对抗网络（GANs）、扩散模型和大型多模态模型的快速发展，AI已经能够创作出令人惊叹的绘画、插图、设计和其他视觉艺术作品。本章将详细介绍AI艺术创作的基本原理、主要应用场景以及实用的使用示例，帮助你掌握如何利用AI进行艺术创作和设计。

## AI艺术创作的基本原理

AI艺术创作主要基于深度学习技术，特别是生成模型。这些模型通过学习大量的艺术作品数据，掌握了艺术风格、构图、色彩运用等特征，并能够生成具有类似特性的新艺术作品。

### 主要技术方法

- **生成对抗网络（GANs）**：通过生成器和判别器的对抗训练生成艺术作品
- **扩散模型（Diffusion Models）**：通过迭代降噪过程生成高质量图像
- **变分自编码器（VAEs）**：学习图像的潜在表示并生成新样本
- **神经风格迁移（Neural Style Transfer）**：将一种艺术风格应用到另一种内容上
- **大型多模态模型**：结合文本和图像理解生成符合描述的艺术作品

### 核心技术原理

#### 艺术生成的工作原理
1. **数据准备**：收集和预处理大量的艺术作品数据
2. **模型训练**：使用艺术数据训练深度生成模型
3. **条件控制**：提供文本描述、风格参考等条件引导生成过程
4. **图像生成**：根据输入条件生成新的艺术图像
5. **后处理**：对生成的图像进行优化和调整
6. **评估与筛选**：评估生成图像的质量并筛选最佳结果

#### 常用的AI艺术生成模型

- **DALL-E 2/3**：OpenAI开发的文本到图像生成模型，能够根据文本描述生成高质量图像
- **Midjourney**：基于Discord的AI艺术生成平台，擅长生成艺术风格的图像
- **Stable Diffusion**：开源的文本到图像扩散模型，可本地部署和定制
- **Imagen**：Google开发的高保真文本到图像生成模型
- **Adobe Firefly**：Adobe开发的创意生成AI工具，与Creative Cloud集成
- **Runway**：提供多种AI创意工具的平台，包括图像生成和视频编辑
- **DreamStudio**：Stable Diffusion的官方Web界面
- **Leonardo.AI**：专注于游戏和创意产业的AI艺术平台

## AI艺术创作的应用场景

AI艺术创作技术已经在多个领域得到广泛应用，以下是一些常见的应用场景：

### 1. 概念艺术和创意设计
- 为电影、游戏和动画创建概念艺术
- 设计角色、场景和道具
- 快速生成创意草图和原型
- 探索不同的艺术风格和视觉表现
- 辅助创意团队进行头脑风暴

### 2. 插画和漫画创作
- 生成书籍和文章的插图
- 辅助漫画创作和故事板设计
- 为社交媒体内容创建视觉元素
- 设计角色形象和背景场景
- 自动生成不同风格的插画作品

### 3. 广告和营销设计
- 创建广告素材和营销图像
- 设计品牌标识和视觉元素
- 生成产品包装和宣传材料
- 制作社交媒体营销内容
- 快速迭代和测试不同的设计方案

### 4. 室内和建筑设计
- 生成室内设计效果图
- 辅助建筑设计和规划
- 展示不同的装修风格和材料
- 快速生成空间布局方案
- 创建虚拟建筑漫游和展示

### 5. 时尚和服装设计
- 设计服装款式和图案
- 创建时尚插图和宣传材料
- 生成面料图案和纹理
- 辅助配饰和鞋类设计
- 预测和展示时尚趋势

### 6. 教育和学习
- 为教育内容创建视觉辅助材料
- 辅助艺术教学和技能培训
- 生成艺术参考和学习资源
- 模拟不同艺术流派和风格
- 为学生提供创意反馈和指导

### 7. 内容创作和媒体
- 为网站和应用程序创建视觉内容
- 生成视频缩略图和封面图像
- 设计UI/UX元素和图标
- 创建数字艺术作品和收藏品
- 辅助内容创作者制作视觉素材

### 8. 个人创意表达
- 为个人项目创建艺术作品
- 探索个人艺术风格和表达
- 制作个性化礼品和纪念品
- 创建数字肖像和自画像
- 作为创意表达的辅助工具

## 基础艺术生成示例

下面是一个使用Python和常用的AI艺术生成API进行基础艺术创作的实现示例：

```python
import os
import requests
import base64
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
import openai

class AIArtGenerator:
    def __init__(self, openai_api_key=None, stability_api_key=None):
        # 初始化API密钥
        if openai_api_key:
            openai.api_key = openai_api_key
        elif 'OPENAI_API_KEY' in os.environ:
            openai.api_key = os.environ['OPENAI_API_KEY']
        else:
            print("警告：未提供OpenAI API密钥，DALL-E功能可能无法使用")
            self.openai_available = False
        
        if stability_api_key:
            self.stability_api_key = stability_api_key
        elif 'STABILITY_API_KEY' in os.environ:
            self.stability_api_key = os.environ['STABILITY_API_KEY']
        else:
            print("警告：未提供Stability API密钥，Stable Diffusion功能可能无法使用")
            self.stability_available = False
        
        # 设置输出目录
        self.output_dir = "output_art"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        # 设置默认参数
        self.default_model = "dall-e-3"
        self.default_size = "1024x1024"
        self.default_quality = "standard"
        self.default_steps = 30
        
    def generate_image_with_dalle(self, prompt, size=None, quality=None, model=None):
        """
        使用OpenAI的DALL-E生成图像
        prompt: 文本描述
        size: 图像尺寸，支持"256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"
        quality: 图像质量，支持"standard"或"hd"
        model: 使用的模型，支持"dall-e-2"或"dall-e-3"
        """
        if not hasattr(self, 'openai_available') or not self.openai_available:
            print("错误：需要OpenAI API密钥才能使用DALL-E功能")
            return None
        
        try:
            # 使用默认值或提供的值
            model = model or self.default_model
            size = size or self.default_size
            quality = quality or self.default_quality
            
            # 调用OpenAI API
            response = openai.Image.create(
                prompt=prompt,
                model=model,
                n=1,
                size=size,
                quality=quality
            )
            
            # 获取图像URL
            image_url = response['data'][0]['url']
            
            # 下载图像
            image_response = requests.get(image_url)
            image = Image.open(BytesIO(image_response.content))
            
            # 保存图像
            timestamp = os.path.basename(image_url).split('.')[0].split('-')[-1]
            output_file = os.path.join(self.output_dir, f"dalle_{timestamp}.png")
            image.save(output_file)
            
            print(f"图像已生成并保存到：{output_file}")
            return output_file
            
        except Exception as e:
            print(f"使用DALL-E生成图像时发生错误: {str(e)}")
            return None
        
    def generate_image_with_stable_diffusion(self, prompt, negative_prompt=None, size=(1024, 1024), steps=None):
        """
        使用Stability AI的Stable Diffusion生成图像
        prompt: 文本描述
        negative_prompt: 不希望在图像中出现的元素
        size: 图像尺寸（宽度, 高度）
        steps: 生成步数
        """
        if not hasattr(self, 'stability_available') or not self.stability_available:
            print("错误：需要Stability API密钥才能使用Stable Diffusion功能")
            return None
        
        try:
            # 使用默认值或提供的值
            steps = steps or self.default_steps
            width, height = size
            
            # 设置API端点
            url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
            
            # 设置请求头
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {self.stability_api_key}"
            }
            
            # 设置请求体
            payload = {
                "text_prompts": [
                    {"text": prompt, "weight": 1}
                ],
                "width": width,
                "height": height,
                "steps": steps,
                "cfg_scale": 7,
                "samples": 1,
                "style_preset": "enhance"
            }
            
            # 如果提供了负面提示词，添加到请求体
            if negative_prompt:
                payload["text_prompts"].append({"text": negative_prompt, "weight": -1})
            
            # 发送请求
            response = requests.post(url, headers=headers, json=payload)
            
            # 检查响应状态
            if response.status_code != 200:
                print(f"API请求失败: {response.text}")
                return None
            
            # 处理响应
            data = response.json()
            
            # 解码并保存图像
            timestamp = str(int(time.time()))
            output_file = os.path.join(self.output_dir, f"stable_diffusion_{timestamp}.png")
            
            for i, image_data in enumerate(data["artifacts"]):
                image = Image.open(BytesIO(base64.b64decode(image_data["base64"])))
                image.save(output_file)
                break  # 只保存第一个图像
            
            print(f"图像已生成并保存到：{output_file}")
            return output_file
            
        except Exception as e:
            print(f"使用Stable Diffusion生成图像时发生错误: {str(e)}")
            return None
        
    def generate_variations(self, image_path, num_variations=4, model="dall-e-2"):
        """
        生成现有图像的变体
        image_path: 原始图像路径
        num_variations: 要生成的变体数量
        model: 使用的模型
        """
        if not hasattr(self, 'openai_available') or not self.openai_available:
            print("错误：需要OpenAI API密钥才能使用此功能")
            return None
        
        try:
            # 检查文件是否存在
            if not os.path.exists(image_path):
                print(f"错误：找不到文件 {image_path}")
                return None
            
            # 打开图像
            with open(image_path, "rb") as image_file:
                # 调用OpenAI API
                response = openai.Image.create_variation(
                    image=image_file,
                    n=num_variations,
                    size="1024x1024",
                    model=model
                )
            
            # 下载并保存每个变体
            output_files = []
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            
            for i, image_data in enumerate(response['data']):
                image_url = image_data['url']
                image_response = requests.get(image_url)
                image = Image.open(BytesIO(image_response.content))
                
                output_file = os.path.join(self.output_dir, f"{base_name}_variation_{i+1}.png")
                image.save(output_file)
                output_files.append(output_file)
                
                print(f"变体 {i+1} 已保存到：{output_file}")
            
            return output_files
            
        except Exception as e:
            print(f"生成图像变体时发生错误: {str(e)}")
            return None
        
    def enhance_image_prompt(self, basic_prompt, style=None, details=None, lighting=None):
        """
        增强图像提示词，使其更具体和详细
        basic_prompt: 基本提示词
        style: 艺术风格
        details: 细节描述
        lighting: 光照效果
        """
        try:
            # 构建增强的提示词
            enhanced_prompt = basic_prompt
            
            if style:
                enhanced_prompt += f", {style}风格"
            
            if details:
                enhanced_prompt += f", {details}"
            
            if lighting:
                enhanced_prompt += f", {lighting}光照"
            
            # 添加一些通用的质量增强词
            enhanced_prompt += ", 高清细节, 最佳质量, 专业创作, 杰作"
            
            return enhanced_prompt
            
        except Exception as e:
            print(f"增强提示词时发生错误: {str(e)}")
            return basic_prompt
        
    def display_image(self, image_path):
        """
        显示生成的图像
        image_path: 图像文件路径
        """
        try:
            # 检查文件是否存在
            if not os.path.exists(image_path):
                print(f"错误：找不到文件 {image_path}")
                return False
            
            # 打开并显示图像
            image = Image.open(image_path)
            plt.figure(figsize=(10, 10))
            plt.imshow(image)
            plt.axis('off')
            plt.title(os.path.basename(image_path))
            plt.show()
            
            return True
            
        except Exception as e:
            print(f"显示图像时发生错误: {str(e)}")
            return False

# 使用示例
if __name__ == "__main__":
    # 导入必要的库
    import time
    
    try:
        # 初始化AI艺术生成器
        art_generator = AIArtGenerator()
        
        # 示例1: 生成简单的图像
        print("\n=== 示例1: 生成简单的图像 ===")
        basic_prompt = "一只在月球上弹钢琴的猫"
        
        # 注意：实际运行时需要有效的API密钥
        # if hasattr(art_generator, 'openai_available') and art_generator.openai_available:
        #     image_file = art_generator.generate_image_with_dalle(
        #         prompt=basic_prompt,
        #         size="1024x1024",
        #         quality="standard",
        #         model="dall-e-3"
        #     )
        #     if image_file:
        #         art_generator.display_image(image_file)
        # else:
        print("提示：DALL-E图像生成功能已配置，但在示例中未实际调用以避免API费用")
        
        # 示例2: 增强提示词并生成图像
        print("\n=== 示例2: 增强提示词并生成图像 ===")
        basic_prompt = "一个未来城市的风景"
        enhanced_prompt = art_generator.enhance_image_prompt(
            basic_prompt=basic_prompt,
            style="赛博朋克",
            details="霓虹灯闪烁，飞行器穿梭，高楼大厦直插云霄",
            lighting="夜晚，霓虹灯照明"
        )
        print(f"增强后的提示词: {enhanced_prompt}")
        
        # 注意：实际运行时需要有效的API密钥
        # if hasattr(art_generator, 'stability_available') and art_generator.stability_available:
        #     image_file = art_generator.generate_image_with_stable_diffusion(
        #         prompt=enhanced_prompt,
        #         negative_prompt="模糊，低质量，变形，像素化",
        #         size=(1024, 768),
        #         steps=30
        #     )
        #     if image_file:
        #         art_generator.display_image(image_file)
        # else:
        print("提示：Stable Diffusion图像生成功能已配置，但在示例中未实际调用以避免API费用")
        
        # 示例3: 生成图像变体
        print("\n=== 示例3: 生成图像变体 ===")
        # 注意：需要提供一个已有的图像文件路径
        # sample_image_path = "path/to/your/image.png"
        # if os.path.exists(sample_image_path):
        #     variation_files = art_generator.generate_variations(sample_image_path, num_variations=2)
        #     for file in variation_files:
        #         art_generator.display_image(file)
        # else:
        print("提示：图像变体生成功能需要提供一个已有的图像文件路径")
        
        # 示例4: 尝试不同的艺术风格
        print("\n=== 示例4: 尝试不同的艺术风格 ===")
        subject = "一棵古老的大树"
        styles = ["印象派", "现实主义", "卡通", "油画", "水彩画"]
        
        for style in styles:
            style_prompt = art_generator.enhance_image_prompt(
                basic_prompt=subject,
                style=style,
                details="枝叶茂盛，周围有小动物",
                lighting="阳光明媚的下午"
            )
            print(f"\n风格: {style}\n提示词: {style_prompt}")
            # 在实际应用中，可以使用这个提示词生成图像
            
    except ImportError as e:
        print(f"缺少必要的库: {str(e)}")
        print("请安装所需依赖: pip install requests matplotlib pillow openai")
        
    except Exception as e:
        print(f"程序运行出错: {str(e)}")
        
    print("\n提示：")
    print("1. 确保已安装所需依赖: pip install requests matplotlib pillow openai")
    print("2. 使用DALL-E功能时，需要设置有效的OpenAI API密钥")
    print("3. 使用Stable Diffusion功能时，需要设置有效的Stability AI API密钥")
    print("4. 提示词越详细、具体，生成的图像质量通常越好")
    print("5. 尝试不同的参数组合可以获得多样化的结果")
    print("6. 生成的图像可以用于个人或商业项目，但请注意版权问题")
```

## 高级艺术创作功能

除了基础的图像生成功能，AI还可以实现更高级的艺术创作功能，如风格迁移、图像修复和扩展等。下面是一个高级艺术创作的示例：

```python
import os
import requests
import base64
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import openai
import cv2

class AdvancedAIArtGenerator:
    def __init__(self, openai_api_key=None, stability_api_key=None):
        # 初始化API密钥
        if openai_api_key:
            openai.api_key = openai_api_key
        elif 'OPENAI_API_KEY' in os.environ:
            openai.api_key = os.environ['OPENAI_API_KEY']
        else:
            print("警告：未提供OpenAI API密钥，某些功能可能无法使用")
            self.openai_available = False
        
        if stability_api_key:
            self.stability_api_key = stability_api_key
        elif 'STABILITY_API_KEY' in os.environ:
            self.stability_api_key = os.environ['STABILITY_API_KEY']
        else:
            print("警告：未提供Stability API密钥，某些功能可能无法使用")
            self.stability_available = False
        
        # 设置输出目录
        self.output_dir = "advanced_output_art"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        # 导入其他必要的库（如果可用）
        self.cv2_available = False
        try:
            import cv2
            self.cv2_available = True
        except ImportError:
            print("警告：未安装OpenCV，某些图像处理功能可能无法使用")
        
    def image_style_transfer(self, content_image_path, style_image_path, output_size=(1024, 1024)):
        """
        图像风格迁移
        content_image_path: 内容图像路径
        style_image_path: 风格图像路径
        output_size: 输出图像尺寸
        """
        if not self.cv2_available:
            print("错误：需要安装OpenCV才能使用此功能")
            return None
        
        try:
            # 导入cv2（在函数内部导入以避免初始化时的错误）
            import cv2
            import numpy as np
            
            # 读取图像
            content_image = cv2.imread(content_image_path)
            style_image = cv2.imread(style_image_path)
            
            # 检查图像是否成功读取
            if content_image is None:
                print(f"错误：无法读取内容图像 {content_image_path}")
                return None
            if style_image is None:
                print(f"错误：无法读取风格图像 {style_image_path}")
                return None
            
            # 调整图像大小
            content_image = cv2.resize(content_image, output_size)
            style_image = cv2.resize(style_image, output_size)
            
            # 将图像转换为浮点型并归一化
            content_image = content_image.astype(np.float32) / 255.0
            style_image = style_image.astype(np.float32) / 255.0
            
            # 加载预训练的VGG19模型（简化实现，实际项目中可能需要更复杂的实现）
            # 这里使用OpenCV的stylization函数作为示例
            # 注意：这是一个简化的风格迁移实现
            output_image = cv2.stylization(content_image, sigma_s=150, sigma_r=0.25)
            
            # 将输出图像保存
            output_file = os.path.join(self.output_dir, f"style_transfer_{int(time.time())}.png")
            
            # 将图像从float32转换回uint8并保存
            output_image_uint8 = (output_image * 255).astype(np.uint8)
            cv2.imwrite(output_file, output_image_uint8)
            
            print(f"风格迁移后的图像已保存到：{output_file}")
            return output_file
            
        except Exception as e:
            print(f"进行图像风格迁移时发生错误: {str(e)}")
            return None
        
    def inpaint_image(self, image_path, mask_path=None, prompt=None, area_to_inpaint=None):
        """
        图像修复
        image_path: 需要修复的图像路径
        mask_path: 掩码图像路径
        prompt: 修复区域的文本描述
        area_to_inpaint: 要修复的区域坐标 (x1, y1, x2, y2)
        """
        if not hasattr(self, 'openai_available') or not self.openai_available:
            print("错误：需要OpenAI API密钥才能使用此功能")
            return None
        
        try:
            # 检查文件是否存在
            if not os.path.exists(image_path):
                print(f"错误：找不到文件 {image_path}")
                return None
            
            # 打开图像
            image = Image.open(image_path)
            width, height = image.size
            
            # 创建掩码（如果未提供）
            if mask_path is None:
                if area_to_inpaint is None:
                    # 默认创建一个中心区域的掩码
                    center_x, center_y = width // 2, height // 2
                    mask_size = min(width, height) // 4
                    area_to_inpaint = (center_x - mask_size, center_y - mask_size, 
                                      center_x + mask_size, center_y + mask_size)
                
                # 创建掩码图像
                mask = Image.new('RGBA', (width, height), color=(0, 0, 0, 0))
                draw = ImageDraw.Draw(mask)
                draw.rectangle(area_to_inpaint, fill=(255, 255, 255, 255))
                
                # 保存掩码图像
                mask_file = os.path.join(self.output_dir, f"mask_{int(time.time())}.png")
                mask.save(mask_file)
                mask_path = mask_file
            
            # 读取图像和掩码
            with open(image_path, "rb") as image_file, open(mask_path, "rb") as mask_file:
                # 调用OpenAI API
                response = openai.Image.create_edit(
                    image=image_file,
                    mask=mask_file,
                    prompt=prompt or "填充缺失部分，使其与周围环境协调",
                    n=1,
                    size="1024x1024"
                )
            
            # 下载并保存修复后的图像
            image_url = response['data'][0]['url']
            image_response = requests.get(image_url)
            repaired_image = Image.open(BytesIO(image_response.content))
            
            output_file = os.path.join(self.output_dir, f"repaired_image_{int(time.time())}.png")
            repaired_image.save(output_file)
            
            print(f"修复后的图像已保存到：{output_file}")
            return output_file
            
        except Exception as e:
            print(f"修复图像时发生错误: {str(e)}")
            return None
        
    def expand_image(self, image_path, direction="all", prompt=None, expansion_ratio=0.25):
        """
        扩展图像边界
        image_path: 需要扩展的图像路径
        direction: 扩展方向，可选 "all", "left", "right", "top", "bottom"
        prompt: 扩展区域的文本描述
        expansion_ratio: 扩展比例（相对于原图像大小）
        """
        if not self.cv2_available:
            print("错误：需要安装OpenCV才能使用此功能")
            return None
        
        try:
            # 导入cv2
            import cv2
            import numpy as np
            
            # 读取图像
            image = cv2.imread(image_path)
            
            # 检查图像是否成功读取
            if image is None:
                print(f"错误：无法读取图像 {image_path}")
                return None
            
            # 获取原图像尺寸
            height, width = image.shape[:2]
            
            # 计算扩展后的尺寸
            expand_width = int(width * expansion_ratio)
            expand_height = int(height * expansion_ratio)
            
            # 根据方向创建新的空白图像
            if direction == "all":
                new_width = width + 2 * expand_width
                new_height = height + 2 * expand_height
                new_image = np.zeros((new_height, new_width, 3), dtype=np.uint8)
                # 将原图放置在中心
                new_image[expand_height:expand_height+height, expand_width:expand_width+width] = image
                # 计算需要填充的区域
                regions = [
                    (0, 0, new_width, expand_height),                           # 顶部
                    (0, expand_height+height, new_width, new_height),           # 底部
                    (0, expand_height, expand_width, expand_height+height),     # 左侧
                    (expand_width+width, expand_height, new_width, expand_height+height)  # 右侧
                ]
            else:
                # 其他方向的实现（简化版）
                # 在实际项目中，可能需要更复杂的处理
                new_width = width
                new_height = height
                if direction in ["left", "right"]:
                    new_width = width + expand_width
                if direction in ["top", "bottom"]:
                    new_height = height + expand_height
                
                new_image = np.zeros((new_height, new_width, 3), dtype=np.uint8)
                
                # 将原图放置在适当位置
                x_offset = 0 if direction != "right" else expand_width
                y_offset = 0 if direction != "bottom" else expand_height
                new_image[y_offset:y_offset+height, x_offset:x_offset+width] = image
                
                # 设置需要填充的区域
                regions = []
                if direction == "left":
                    regions.append((0, 0, expand_width, new_height))
                elif direction == "right":
                    regions.append((width, 0, new_width, new_height))
                elif direction == "top":
                    regions.append((0, 0, new_width, expand_height))
                elif direction == "bottom":
                    regions.append((0, height, new_width, new_height))
            
            # 在实际项目中，这里应该使用AI模型填充扩展区域
            # 这里使用简单的边界扩展作为示例
            # 注意：这是一个简化的实现
            for region in regions:
                x1, y1, x2, y2 = region
                # 简单的边界复制扩展（在实际项目中应使用更复杂的算法）
                # 这里仅作为占位符
                pass
            
            # 将OpenCV图像转换为PIL图像进行显示和保存
            new_image_pil = Image.fromarray(cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB))
            
            # 保存扩展后的图像
            output_file = os.path.join(self.output_dir, f"expanded_image_{int(time.time())}.png")
            new_image_pil.save(output_file)
            
            print(f"扩展后的图像已保存到：{output_file}")
            print("提示：这是一个简化的图像扩展实现，实际项目中应使用专门的AI模型进行内容感知扩展")
            return output_file
            
        except Exception as e:
            print(f"扩展图像时发生错误: {str(e)}")
            return None
        
    def generate_multi_concept_image(self, concepts, composition=None, style=None, size=(1024, 1024)):
        """
        生成包含多个概念的复杂图像
        concepts: 概念列表，每个概念包含描述和位置
        composition: 构图描述
        style: 艺术风格
        size: 输出图像尺寸
        """
        if not hasattr(self, 'openai_available') or not self.openai_available:
            print("错误：需要OpenAI API密钥才能使用此功能")
            return None
        
        try:
            # 构建详细的提示词
            prompt = ""
            
            # 添加风格描述
            if style:
                prompt += f"{style}风格，"
            
            # 添加构图描述
            if composition:
                prompt += f"{composition}，"
            
            # 添加概念描述
            prompt += "包含以下元素："
            for concept in concepts:
                concept_desc = concept.get('description', '')
                concept_pos = concept.get('position', '')
                if concept_pos:
                    prompt += f"在{concept_pos}的{concept_desc}，"
                else:
                    prompt += f"{concept_desc}，"
            
            # 添加质量描述
            prompt += "高清细节，最佳质量，专业创作，杰作"
            
            print(f"构建的提示词: {prompt}")
            
            # 调用OpenAI API
            response = openai.Image.create(
                prompt=prompt,
                model="dall-e-3",
                n=1,
                size=f"{size[0]}x{size[1]}",
                quality="hd"
            )
            
            # 下载并保存图像
            image_url = response['data'][0]['url']
            image_response = requests.get(image_url)
            image = Image.open(BytesIO(image_response.content))
            
            output_file = os.path.join(self.output_dir, f"multi_concept_image_{int(time.time())}.png")
            image.save(output_file)
            
            print(f"包含多个概念的图像已保存到：{output_file}")
            return output_file
            
        except Exception as e:
            print(f"生成包含多个概念的图像时发生错误: {str(e)}")
            return None
        
    def generate_storyboard(self, story, num_frames=5, style=None):
        """
        生成故事板
        story: 故事描述或情节大纲
        num_frames: 要生成的帧数
        style: 艺术风格
        """
        if not hasattr(self, 'openai_available') or not self.openai_available:
            print("错误：需要OpenAI API密钥才能使用此功能")
            return None
        
        try:
            # 先让GPT-4分析故事并提取关键场景
            scene_prompt = f"""\请分析以下故事，并提取{num_frames}个最关键的场景，用于创建故事板。
            
            故事：
            {story}
            
            请以简洁的描述返回这{num_frames}个场景，每个场景一行，不要包含任何额外的解释或说明。
            """
            
            # 调用OpenAI API分析故事
            scene_response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "你是一位专业的故事板艺术家，擅长分析故事并提取关键场景。"},
                    {"role": "user", "content": scene_prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            # 提取场景描述
            scenes_text = scene_response['choices'][0]['message']['content']
            scenes = scenes_text.strip().split('\n')
            
            print(f"提取的{num_frames}个关键场景：")
            for i, scene in enumerate(scenes):
                print(f"场景{i+1}: {scene}")
            
            # 为每个场景生成图像
            storyboard_files = []
            for i, scene in enumerate(scenes):
                # 构建场景提示词
                scene_prompt = scene
                if style:
                    scene_prompt += f", {style}风格"
                scene_prompt += ", 高清细节，最佳质量，故事板帧，清晰的构图，明确的视觉叙事"
                
                print(f"\n正在生成场景{i+1}的图像...")
                
                # 调用OpenAI API生成图像
                image_response = openai.Image.create(
                    prompt=scene_prompt,
                    model="dall-e-3",
                    n=1,
                    size="1024x1024",
                    quality="standard"
                )
                
                # 下载并保存图像
                image_url = image_response['data'][0]['url']
                img_response = requests.get(image_url)
                image = Image.open(BytesIO(img_response.content))
                
                output_file = os.path.join(self.output_dir, f"storyboard_frame_{i+1}_{int(time.time())}.png")
                image.save(output_file)
                storyboard_files.append(output_file)
                
                print(f"场景{i+1}的图像已保存到：{output_file}")
                
            # 创建一个故事板拼贴图（简化版）
            if len(storyboard_files) > 0:
                # 读取所有帧
                frames = [Image.open(file) for file in storyboard_files]
                
                # 计算拼贴图尺寸
                frame_width, frame_height = frames[0].size
                collage_width = frame_width * min(3, len(frames))  # 每行最多3帧
                collage_height = frame_height * ((len(frames) + 2) // 3)  # 向上取整计算行数
                
                # 创建空白拼贴图
                collage = Image.new('RGB', (collage_width, collage_height), color=(255, 255, 255))
                
                # 粘贴每帧图像
                for i, frame in enumerate(frames):
                    row = i // 3
                    col = i % 3
                    x = col * frame_width
                    y = row * frame_height
                    collage.paste(frame, (x, y))
                
                # 保存拼贴图
                collage_file = os.path.join(self.output_dir, f"storyboard_collage_{int(time.time())}.png")
                collage.save(collage_file)
                
                print(f"故事板拼贴图已保存到：{collage_file}")
                storyboard_files.append(collage_file)
                
            return storyboard_files
            
        except Exception as e:
            print(f"生成故事板时发生错误: {str(e)}")
            return None

# 使用示例
if __name__ == "__main__":
    # 导入必要的库
    import time
    
    try:
        # 初始化高级AI艺术生成器
        advanced_art_generator = AdvancedAIArtGenerator()
        
        # 示例1: 图像风格迁移
        print("\n=== 示例1: 图像风格迁移 ===")
        # 注意：需要提供内容图像和风格图像的路径
        # content_image_path = "path/to/content/image.jpg"
        # style_image_path = "path/to/style/image.jpg"
        # if os.path.exists(content_image_path) and os.path.exists(style_image_path):
        #     styled_image = advanced_art_generator.image_style_transfer(content_image_path, style_image_path)
        # else:
        print("提示：图像风格迁移功能需要提供内容图像和风格图像的路径")
        
        # 示例2: 图像修复
        print("\n=== 示例2: 图像修复 ===")
        # 注意：需要提供要修复的图像路径
        # image_to_repair = "path/to/image/with/missing/parts.jpg"
        # prompt = "将缺失部分填充为与周围环境协调的内容"
        # if hasattr(advanced_art_generator, 'openai_available') and advanced_art_generator.openai_available:
        #     if os.path.exists(image_to_repair):
        #         repaired_image = advanced_art_generator.inpaint_image(image_to_repair, prompt=prompt)
        # else:
        print("提示：图像修复功能需要有效的OpenAI API密钥和要修复的图像路径")
        
        # 示例3: 扩展图像边界
        print("\n=== 示例3: 扩展图像边界 ===")
        # 注意：需要提供要扩展的图像路径
        # image_to_expand = "path/to/image/to/expand.jpg"
        # if os.path.exists(image_to_expand):
        #     expanded_image = advanced_art_generator.expand_image(image_to_expand, direction="all")
        # else:
        print("提示：图像扩展功能需要提供要扩展的图像路径")
        
        # 示例4: 生成包含多个概念的图像
        print("\n=== 示例4: 生成包含多个概念的图像 ===")
        concepts = [
            {"description": "穿着宇航服的宇航员", "position": "画面中央"},
            {"description": "巨大的机器人", "position": "宇航员右侧"},
            {"description": "未来城市的远景", "position": "背景"}
        ]
        composition = "电影般的广角镜头，戏剧性的照明"
        style = "科幻电影海报"
        
        # 注意：实际运行时需要有效的OpenAI API密钥
        # if hasattr(advanced_art_generator, 'openai_available') and advanced_art_generator.openai_available:
        #     multi_concept_image = advanced_art_generator.generate_multi_concept_image(
        #         concepts=concepts,
        #         composition=composition,
        #         style=style
        #     )
        # else:
        print("提示：生成包含多个概念的图像功能需要有效的OpenAI API密钥")
        
        # 示例5: 生成故事板
        print("\n=== 示例5: 生成故事板 ===")
        story = """
        一个年轻的探险家在森林中发现了一个神秘的门户。她决定进入门户，发现自己来到了一个奇幻世界。在那里，她遇到了会说话的动物，并得知自己是预言中的英雄，需要拯救这个世界免受黑暗力量的侵害。她踏上了冒险之旅，学习新的技能，并最终与黑暗力量展开了决战。
        """
        
        # 注意：实际运行时需要有效的OpenAI API密钥
        # if hasattr(advanced_art_generator, 'openai_available') and advanced_art_generator.openai_available:
        #     storyboard_files = advanced_art_generator.generate_storyboard(
        #         story=story,
        #         num_frames=5,
        #         style="水彩画"
        #     )
        # else:
        print("提示：生成故事板功能需要有效的OpenAI API密钥")
        
    except ImportError as e:
        print(f"缺少必要的库: {str(e)}")
        print("请安装所需依赖: pip install requests matplotlib pillow openai opencv-python")
        
    except Exception as e:
        print(f"程序运行出错: {str(e)}")
        
    print("\n提示：")
    print("1. 确保已安装所需依赖: pip install requests matplotlib pillow openai opencv-python")
    print("2. 高级艺术创作功能通常需要更强大的模型和更多的API调用")
    print("3. 为获得最佳效果，提供详细、具体的提示词和上下文信息")
    print("4. 对于复杂的创作任务，考虑分步骤进行，先生成草图再细化")
    print("5. 组合使用不同的AI工具可以实现更复杂的创作目标")
    print("6. 始终注意生成内容的版权和伦理问题")
```

## 最佳实践

使用AI进行艺术创作时，以下是一些最佳实践：

### 1. 掌握提示词艺术
- 使用具体、详细的描述语言
- 包含视觉元素、构图、色彩、光照等细节
- 学习和使用艺术术语和风格参考
- 尝试不同的提示词组合和表达方式
- 使用负面提示词排除不想要的元素

### 2. 明确创作目标
- 确定艺术作品的用途和目标受众
- 明确所需的艺术风格和视觉效果
- 考虑作品的构图和布局要求
- 设定合理的分辨率和尺寸
- 规划创作的步骤和流程

### 3. 迭代优化
- 从小规模的测试开始
- 根据生成结果逐步调整提示词
- 尝试不同的模型和参数组合
- 保存和比较不同的生成结果
- 对满意的结果进行进一步细化

### 4. 结合人工创作
- 将AI生成作为创意起点而非终点
- 对生成的作品进行人工编辑和调整
- 添加个人创意和艺术风格
- 使用专业工具进行后期处理
- 结合传统艺术技巧和AI技术

### 5. 学习艺术基础知识
- 了解基本的构图原则
- 学习色彩理论和搭配技巧
- 熟悉不同艺术流派和风格的特点
- 掌握基本的透视和光影知识
- 学习视觉叙事和故事板设计

### 6. 利用专业工具
- 使用图像编辑软件进行后期处理
- 利用设计工具组合和优化AI生成内容
- 使用3D建模软件增强视觉效果
- 学习使用专业的调色和滤镜工具
- 掌握文件格式和输出设置

### 7. 版权和伦理考虑
- 了解AI生成内容的版权归属问题
- 确保不侵犯他人的知识产权
- 注明AI在创作过程中的作用
- 尊重AI训练数据中包含的原创作品
- 考虑生成内容的社会和文化影响

### 8. 持续学习和实践
- 关注AI艺术技术的最新发展
- 学习和借鉴其他创作者的经验和技巧
- 参与AI艺术社区和讨论
- 定期练习和实验新的创作方法
- 记录和分享自己的创作过程和发现

## 总结

AI艺术创作技术正在为创意领域带来革命性的变化，为艺术家、设计师和创意工作者提供了强大的创作工具和灵感来源。从简单的图像生成到复杂的艺术创作，AI已经能够支持视觉艺术创作的各个环节，帮助创作者探索新的艺术可能性。

随着生成模型和多模态技术的不断进步，未来的AI艺术创作工具将更加智能、灵活和专业，能够更好地理解和实现创作者的意图，生成更高质量、更具表现力的艺术作品。对于创意工作者来说，掌握AI艺术创作技术将成为提升创作效率和拓展创作领域的重要技能。

然而，我们也应该认识到，AI艺术创作技术是辅助创作的工具，而非替代人类创造力的手段。真正优秀的艺术作品仍然需要人类的情感表达、创意构思和艺术判断。通过将AI技术与人类创造力相结合，我们可以开拓艺术创作的新边界，创造出更加丰富多彩的艺术作品。

无论是专业艺术家还是艺术爱好者，都可以利用AI艺术创作技术来激发创意、提高效率、探索新的艺术风格和可能性。随着技术的不断发展和普及，AI艺术创作将成为创意领域不可或缺的一部分，为艺术世界带来更多惊喜和创新。