import os
import subprocess


def 贴图格式转换(file_path, 输出格式大写="PNG"):

    原始文件目录 = os.path.dirname(file_path)
    转换格式后文件路径 = os.path.splitext(file_path)[0] + "." + 输出格式大写

    # 当前脚本目录 = os.path.split(os.path.realpath(__file__))[0]
    转换器 = os.path.split(os.path.realpath(__file__))[0] + "\\" + "texconv.exe"
    cmd代码 = "\"" + 转换器 + "\"" + " -ft " + 输出格式大写 + " " + \
        "\"" + file_path + "\"" + " -o " + "\"" + 原始文件目录 + "\""
    # print(cmd代码)
    # print(subprocess.call(cmd代码))
    subprocess.call(cmd代码)
    return 转换格式后文件路径


if __name__ == "__main__":
    # print("当前脚本目录", 当前脚本目录)
    # print("转换器", 转换器)
    file_path = "E:\\Unpack_Files\\Gujian3_old\\asset\\characters\\actress2\\textures\\actress2_bx_body_01d.dds"
    convert(file_path)
    """
    Usage: texconv <options> <files>

    -r                  wildcard filename search is recursive
    -flist <filename>   use text file with a list of input files (one per line)

    -w <n>              width
    -h <n>              height
    -m <n>              miplevels
    -f <format>         format

    -if <filter>        image filtering
    -srgb{i|o}          sRGB {input, output}

    -px <string>        name prefix
    -sx <string>        name suffix
    -o <directory>      output directory
    -l                  force output filename to lower case
    -y                  overwrite existing output file (if any)
    -ft <filetype>      output file type

    -hflip              horizonal flip of source image
    -vflip              vertical flip of source image

    -sepalpha           resize/generate mips alpha channel separately
                        from color channels
    -keepcoverage <ref> Preserve alpha coverage in mips for alpha test ref

    -nowic              Force non-WIC filtering
    -wrap, -mirror      texture addressing mode (wrap, mirror, or clamp)
    -pmalpha            convert final texture to use premultiplied alpha
    -alpha              convert premultiplied alpha to straight alpha
    -at <threshold>     Alpha threshold used for BC1, RGBA5551, and WIC
                        (defaults to 0.5)

    -fl <feature-level> Set maximum feature level target (defaults to 11.0)
    -pow2               resize to fit a power-of-2, respecting aspect ratio

    -nmap <options>     converts height-map to normal-map
                        options must be one or more of
                            r, g, b, a, l, m, u, v, i, o
    -nmapamp <weight>   normal map amplitude (defaults to 1.0)

                        (DDS input only)
    -t{u|f}             TYPELESS format is treated as UNORM or FLOAT
    -dword              Use DWORD instead of BYTE alignment
    -badtails           Fix for older DXTn with bad mipchain tails
    -fixbc4x4           Fix for odd-sized BC files that Direct3D can't load
    -xlum               expand legacy L8, L16, and A8P8 formats

                        (DDS output only)
    -dx10               Force use of 'DX10' extended header
    -dx9                Force use of legacy DX9 header

                        (TGA output only)
    -tga20              Write file including TGA 2.0 extension area

                        (BMP, PNG, JPG, TIF, WDP output only)
    -wicq <quality>     When writing images with WIC use quality (0.0 to 1.0)
    -wiclossless        When writing images with WIC use lossless mode
    -wicmulti           When writing images with WIC encode multiframe images

    -nologo             suppress copyright message
    -timing             Display elapsed processing time

    -singleproc         Do not use multi-threaded compression
    -gpu <adapter>      Select GPU for DirectCompute-based codecs (0 is default)
    -nogpu              Do not use DirectCompute-based codecs

    -bc <options>       Sets options for BC compression
                        options must be one or more of
                            d, u, q, x
    -aw <weight>        BC7 GPU compressor weighting for alpha error metric
                        (defaults to 1.0)

    -c <hex-RGB>        colorkey (a.k.a. chromakey) transparency
    -rotatecolor <rot>  rotates color primaries and/or applies a curve
    -nits <value>       paper-white value in nits to use for HDR10 (def: 200.0)
    -tonemap            Apply a tonemap operator based on maximum luminance
    -x2bias             Enable *2 - 1 conversion cases for unorm/pos-only-float
    -inverty            Invert Y (i.e. green) channel values

    <format>: R32G32B32A32_FLOAT R32G32B32A32_UINT R32G32B32A32_SINT
        R32G32B32_FLOAT R32G32B32_UINT R32G32B32_SINT R16G16B16A16_FLOAT
        R16G16B16A16_UNORM R16G16B16A16_UINT R16G16B16A16_SNORM
        R16G16B16A16_SINT R32G32_FLOAT R32G32_UINT R32G32_SINT
        R10G10B10A2_UNORM R10G10B10A2_UINT R11G11B10_FLOAT R8G8B8A8_UNORM
        R8G8B8A8_UNORM_SRGB R8G8B8A8_UINT R8G8B8A8_SNORM R8G8B8A8_SINT
        R16G16_FLOAT R16G16_UNORM R16G16_UINT R16G16_SNORM R16G16_SINT
        R32_FLOAT R32_UINT R32_SINT R8G8_UNORM R8G8_UINT R8G8_SNORM
        R8G8_SINT R16_FLOAT R16_UNORM R16_UINT R16_SNORM R16_SINT
        R8_UNORM R8_UINT R8_SNORM R8_SINT A8_UNORM R9G9B9E5_SHAREDEXP
        R8G8_B8G8_UNORM G8R8_G8B8_UNORM BC1_UNORM BC1_UNORM_SRGB BC2_UNORM
        BC2_UNORM_SRGB BC3_UNORM BC3_UNORM_SRGB BC4_UNORM BC4_SNORM
        BC5_UNORM BC5_SNORM B5G6R5_UNORM B5G5R5A1_UNORM B8G8R8A8_UNORM
        B8G8R8X8_UNORM R10G10B10_XR_BIAS_A2_UNORM B8G8R8A8_UNORM_SRGB
        B8G8R8X8_UNORM_SRGB BC6H_UF16 BC6H_SF16 BC7_UNORM BC7_UNORM_SRGB
        AYUV Y410 Y416 YUY2 Y210 Y216 B4G4R4A4_UNORM
        DXT1 DXT2 DXT3 DXT4 DXT5 RGBA BGRA FP16 FP32 BPTC
        BPTC_FLOAT

    <filter>: POINT LINEAR CUBIC FANT BOX TRIANGLE POINT_DITHER
        LINEAR_DITHER CUBIC_DITHER FANT_DITHER BOX_DITHER TRIANGLE_DITHER
        POINT_DITHER_DIFFUSION LINEAR_DITHER_DIFFUSION CUBIC_DITHER_DIFFUSION
        FANT_DITHER_DIFFUSION BOX_DITHER_DIFFUSION TRIANGLE_DITHER_DIFFUSION

    <rot>: 709to2020 2020to709 709toHDR10 HDR10to709 P3to2020
        P3toHDR10

    <filetype>: BMP JPG JPEG PNG DDS TGA HDR TIF TIFF WDP HDP JXR

    <feature-level>: 9.1 9.2 9.3 10.0 10.1 11.0 11.1 12.0 12.1

    <adapter>:
        0: VID:10DE, PID:1F08 - NVIDIA GeForce RTX 2060
        1: VID:1414, PID:008C - Microsoft Basic Render Driver


    """
