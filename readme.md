# Simple Tetris

学習用の簡単なTetrisゲームをPythonとPygameで実装。

このプロジェクトは仕様駆動開発（Spec-Driven Development）のアプローチを採用し、`.kiro/specs/`ディレクトリに要件定義、設計書、実装タスクを含む包括的な仕様を含んでいます。

## プロジェクト構造

```
.
├── .git/                   # Gitリポジトリ
├── .kiro/                  # Kiro仕様ファイル
│   └── specs/
│       └── simple-tetris/
│           ├── requirements.md  # 要件定義
│           ├── design.md        # 設計書
│           └── tasks.md         # 実装タスク
├── src/                    # ソースコード
│   ├── __init__.py
│   ├── tetromino.py       # Tetrominoクラス
│   ├── game_board.py      # GameBoardクラス
│   ├── game_engine.py     # GameEngineクラス
│   └── game_display.py    # GameDisplayクラス
├── .gitignore             # Git無視ファイル
├── main.py                # メインゲームファイル
├── tetris_single.py       # 1ファイル版（ポータブル）
├── README.md              # このファイル
└── requirements.txt       # 依存関係
```

## セットアップ

1. 依存関係をインストール:
```bash
pip install -r requirements.txt
```

2. ゲームを実行:
```bash
# モジュール版（推奨）
python main.py

# 1ファイル版（ポータブル）
python tetris_single.py
```

## 操作方法

- ←/→: 左右移動
- ↓: 高速落下
- ↑: 回転
- R: ゲームオーバー時にリスタート

## バージョンについて

このプロジェクトには2つのバージョンがあります：

### モジュール版（main.py + src/）
- **推奨**: 開発・学習用
- コードが整理されており、理解しやすい
- 各クラスが独立したファイルに分かれている
- デバッグやカスタマイズが容易

### 1ファイル版（tetris_single.py）
- **ポータブル**: 配布・共有用
- 1つのファイルだけで動作
- 依存関係はpygameのみ
- 簡単に他の環境に移植可能

## 開発について

このプロジェクトは仕様駆動開発を採用しており、以下の仕様ファイルが含まれています：

- **requirements.md**: 機能要件とユーザーストーリー
- **design.md**: システム設計と正確性プロパティ
- **tasks.md**: 実装タスクリスト

仕様ファイルは `.kiro/specs/simple-tetris/` ディレクトリにあります。

## コアクラス

### Tetromino
- 7種類のテトロミノ形状を管理
- 回転と移動機能
- ブロック位置の計算

### GameBoard
- 10×20のゲームフィールド
- 衝突検出
- ライン消去機能

### GameEngine
- ゲームロジックの制御
- 自動落下システム
- 入力処理

### GameDisplay
- Pygameを使用した描画
- ボード、ピース、UIの表示
- ゲームオーバー画面