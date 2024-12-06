from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize

# 定义Cython扩展模块
extensions = [
    Extension(
        "_cwordninja_core",  # 模块名
        sources=["core.pyx"],  # Cython源文件
        extra_compile_args=['-O3'],  # 额外的编译参数
    )
]

# 设置setup参数
setup(
    name='cwordninja',  # 包名
    version='2.0.1',  # 版本号
    author='Your Name',  # 作者
    author_email='your.email@example.com',  # 作者邮箱
    description='A short description of your package',  # 包描述
    long_description='A longer description of your package',  # 长描述
    long_description_content_type='text/markdown',  # 长描述内容类型
    url='https://github.com/yourusername/yourpackagename',  # 项目URL
    packages=["cwordninja"],  # 包名
    ext_modules=cythonize(extensions, compiler_directives={'language_level': "3"}),  # Cython编译选项
    install_requires=[  # 依赖
    ],
    python_requires='>=3.6',  # 兼容的Python版本
    include_package_data=True,  # 包含数据文件
    classifiers=[  # 包分类
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.10',
    ],
)
