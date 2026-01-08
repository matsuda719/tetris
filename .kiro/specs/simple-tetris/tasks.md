# Implementation Plan: Simple Tetris

## Overview

学習用の簡単なTetrisゲームをPythonとPygameを使用して段階的に実装する。各タスクは前のタスクの成果を基に構築され、最終的に完全に動作するTetrisゲームを作成する。

## Tasks

- [x] 1. プロジェクト構造とコアインターフェースの設定
  - プロジェクトディレクトリ構造を作成
  - 必要な依存関係（pygame, hypothesis）をrequirements.txtに定義
  - コアクラスの基本インターフェースを定義
  - _Requirements: 1.1, 1.2_

- [-] 2. Tetrominoクラスの実装
  - [x] 2.1 基本的なTetrominoクラスを実装
    - 7種類のテトロミノ形状データを定義
    - 基本的な移動・回転メソッドを実装
    - _Requirements: 7.1, 7.3_

  - [x] 2.2 Tetromino回転のプロパティテストを作成

    - **Property 2: Tetromino Rotation**
    - **Validates: Requirements 2.4**

  - [x] 2.3 Tetromino形状精度のプロパティテストを作成

    - **Property 11: Shape Accuracy**
    - **Validates: Requirements 7.3**

- [-] 3. GameBoardクラスの実装
  - [x] 3.1 ゲームボードの基本機能を実装
    - 10×20グリッドの初期化
    - 位置検証とピース配置機能
    - ライン消去機能
    - _Requirements: 1.2, 4.1, 4.2, 4.3_

  - [x] 3.2 ライン消去のプロパティテストを作成

    - **Property 6: Line Clearing**
    - **Validates: Requirements 4.1, 4.2, 4.3**

- [x] 4. 衝突検出システムの実装
  - [x] 4.1 衝突検出ロジックを実装
    - 境界チェック機能
    - ブロック間衝突検出
    - 移動・回転の有効性判定
    - _Requirements: 2.5_

  - [x] 4.2 衝突検出のプロパティテストを作成

    - **Property 3: Collision Detection**
    - **Validates: Requirements 2.5**

- [x] 5. チェックポイント - 基本ロジックの確認
  - すべてのテストが通ることを確認し、質問があれば聞く

- [-] 6. GameEngineクラスの実装
  - [x] 6.1 ゲームエンジンのコア機能を実装
    - ゲーム状態管理
    - ピース生成とスポーン
    - 自動落下システム
    - ゲームオーバー検出
    - _Requirements: 1.3, 3.1, 3.2, 3.3, 6.1, 7.2_

  - [x] 6.2 移動機能のプロパティテストを作成

    - **Property 1: Tetromino Movement**
    - **Validates: Requirements 2.1, 2.2, 2.3**

  - [x] 6.3 自動落下のプロパティテストを作成

    - **Property 4: Automatic Fall**
    - **Validates: Requirements 3.1**

  - [x] 6.4 ピース配置のプロパティテストを作成

    - **Property 5: Piece Placement**
    - **Validates: Requirements 3.2, 3.3**

- [x] 7. 入力処理システムの実装
  - [x] 7.1 キーボード入力ハンドラーを実装
    - 矢印キーによる移動・回転処理
    - ゲームオーバー時の入力無効化
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 6.3_

  - [x] 7.2 ゲームオーバー検出のプロパティテストを作成

    - **Property 8: Game Over Detection**
    - **Validates: Requirements 6.1, 6.3**

- [-] 8. GameDisplayクラスの実装
  - [x] 8.1 Pygame表示システムを実装
    - ゲームウィンドウの初期化
    - ボード、ピース、次のピースの描画
    - ゲームオーバー画面の表示
    - _Requirements: 1.1, 5.1, 5.2, 5.3, 5.4, 6.2_

  - [x] 8.2 表示完全性のプロパティテストを作成

    - **Property 7: Display Completeness**
    - **Validates: Requirements 5.1, 5.2, 5.3, 5.4**

  - [x] 8.3 ゲームオーバー表示のプロパティテストを作成

    - **Property 9: Game Over Display**
    - **Validates: Requirements 6.2**

- [x] 9. ランダム生成システムの実装
  - [x] 9.1 Tetrominoランダム生成を実装
    - 7種類からのランダム選択
    - 次のピース予告機能
    - _Requirements: 7.1, 7.2_

  - [x] 9.2 Tetromino生成のプロパティテストを作成

    - **Property 10: Tetromino Generation**
    - **Validates: Requirements 7.1, 7.2**

- [-] 10. メインゲームループの統合
  - [x] 10.1 すべてのコンポーネントを統合
    - メインゲームループの実装
    - 各コンポーネント間の連携
    - ゲーム実行可能ファイルの作成
    - _Requirements: 1.1, 1.2, 1.3_

  - [x] 10.2 統合テストを作成

    - エンドツーエンドのゲームフロー検証
    - _Requirements: 1.1, 1.2, 1.3_

- [x] 11. 最終チェックポイント - 全機能の確認
  - すべてのテストが通ることを確認し、質問があれば聞く

## Notes

- `*`マークのタスクはオプションで、より迅速なMVPのためにスキップ可能
- 各タスクは特定の要件への追跡可能性のために要件を参照
- チェックポイントは段階的な検証を保証
- プロパティテストは普遍的な正確性プロパティを検証
- ユニットテストは特定の例とエッジケースを検証