# T1脳MRIの前処理用コード
法政のT1脳MRIに使用されている前処理の実装です．<br>
ご不明な点がございましたらmackyまでご連絡ください．

## インストール
0. 仮想環境を作成してください．
1. PyTorchをインストールしてください．<br>
https://pytorch.org/
2. git cloneしてください．
```
git clone https://github.com/IyatomiLab/brain-preprocessing.git
cd brain-preprocessing
```
3. ライブラリをインストールしてください．
```
pip install -r requirements.txt
```

## 処理1：頭蓋骨除去とParcellation
頭蓋骨除去とParcellationにはOpenMAP-T1を使います．```-i```にダウンロードしたデータセットのディレクトリ，```-o```に保存先のディレクトリを指定してください．<br>
```-i```で指定したディレクトリ内に存在する.niiファイルを再帰的に探します．
```-o```のディレクトリが存在しない場合は自動で作成されます．
```
python3 1_OpenMAP-T1-V2 -i INPUT_DIRNAME -o OUTPUT_DIRNAME
```

## 処理2：Affine変換による位置合わせ．
Affine変換による位置合わせを行います．<br>
処理1の```-o```で指定したパスを```-i```に指定してください．
```
python3 2_Affine_transform -i INPUT_DIRNAME（処理1のOUTPUT_DIRNAME）
```

## フォルダ構成の例
```
# 取得先（再帰的に取得する）
INPUT_DIRNAME/
  ├ A/
  |   ├ A.nii
  |   ├ B.nii
  |   ├ **.nii
  ├ B/
  |   ├ C.nii
  |   ├ D.nii
      ├ **.nii

# 保存先
OUTPUT_DIRNAME/（処理2のINPUT_DIRNAME）
  ├ unified/ # 頭蓋骨除去された画像（256✕256✕256）
  |   ├ A.nii
  |   ├ B.nii
  |   ├ **.nii
  ├ parcellation/ # parcellationマップ（256✕256✕256）
  |   ├ A.nii
  |   ├ B.nii
  |   ├ **.nii
  ├ full/ # Affine変換後の画像（160✕224✕160）
  |   ├ rigid/
  |   |   ├ A.nii
  |   |   ├ B.nii
  |   |   ├ **.nii
  |   └ trsaa/
  |       ├ A.nii
  |       ├ B.nii
  |       ├ **.nii
  └ half/ # Affine変換後の画像（80✕112✕80）
      ├ rigid/
      |   ├ A.nii
      |   ├ B.nii
      |   ├ **.nii
      └ trsaa/
          ├ A.nii
          ├ B.nii
          ├ **.nii
```
## 引用
脳MRIを使用した研究では必ず前処理のセクションで以下のPaperを引用してください．<br>
Paper: https://www.medrxiv.org/content/10.1101/2024.01.18.24301494v1<br>
```
@article {Nishimaki2024.01.18.24301494,
	author = {Kei Nishimaki and Kengo Onda and Kumpei Ikuta and Yuto Uchida and Susumu Mori and Hitoshi Iyatomi and Kenichi Oishi},
	title = {OpenMAP-T1: A Rapid Deep Learning Approach to Parcellate 280 Anatomical Regions to Cover the Whole Brain},
	elocation-id = {2024.01.18.24301494},
	year = {2024},
	doi = {10.1101/2024.01.18.24301494},
	publisher = {Cold Spring Harbor Laboratory Press},
	URL = {https://www.medrxiv.org/content/early/2024/01/20/2024.01.18.24301494},
	eprint = {https://www.medrxiv.org/content/early/2024/01/20/2024.01.18.24301494.full.pdf},
	journal = {medRxiv}
}
```
