# Requirements Document

## Introduction

学習用の簡単なTetrisゲームをPythonで実装する。基本的なTetrisの機能を持ちつつ、シンプルで理解しやすい構造とする。

## Glossary

- **Game_Engine**: ゲームのメインロジックを管理するシステム
- **Tetromino**: Tetrisで落下するブロック（I、O、T、S、Z、J、Lの7種類）
- **Game_Board**: ゲームフィールド（通常10×20のグリッド）
- **Line_Clear**: 横一列が埋まった時に行を消去する処理
- **Game_Display**: ゲーム画面の表示システム

## Requirements

### Requirement 1

**User Story:** プレイヤーとして、Tetrisゲームを開始できるようにしたい。そうすることで、ゲームを楽しむことができる。

#### Acceptance Criteria

1. WHEN プログラムを実行する THEN Game_Engine SHALL ゲームウィンドウを表示する
2. WHEN ゲームが開始される THEN Game_Board SHALL 10×20のグリッドで初期化される
3. WHEN ゲームが開始される THEN Game_Engine SHALL 最初のTetrominoを生成して表示する

### Requirement 2

**User Story:** プレイヤーとして、Tetrominoを操作できるようにしたい。そうすることで、戦略的にブロックを配置できる。

#### Acceptance Criteria

1. WHEN 左矢印キーが押される THEN Game_Engine SHALL 現在のTetrominoを左に1マス移動する
2. WHEN 右矢印キーが押される THEN Game_Engine SHALL 現在のTetrominoを右に1マス移動する
3. WHEN 下矢印キーが押される THEN Game_Engine SHALL 現在のTetrominoを下に1マス移動する
4. WHEN 上矢印キーが押される THEN Game_Engine SHALL 現在のTetrominoを時計回りに90度回転する
5. WHEN Tetrominoが境界や他のブロックと衝突する THEN Game_Engine SHALL 移動や回転を無効にする

### Requirement 3

**User Story:** プレイヤーとして、Tetrominoが自動的に落下するようにしたい。そうすることで、時間的なプレッシャーを感じながらゲームを楽しめる。

#### Acceptance Criteria

1. THE Game_Engine SHALL 一定間隔でTetrominoを自動的に下に移動する
2. WHEN Tetrominoが底に到達するか他のブロックに衝突する THEN Game_Engine SHALL そのTetrominoを固定する
3. WHEN Tetrominoが固定される THEN Game_Engine SHALL 新しいTetrominoを生成する

### Requirement 4

**User Story:** プレイヤーとして、完成した行が消去されるようにしたい。そうすることで、スコアを獲得し、ゲームを継続できる。

#### Acceptance Criteria

1. WHEN 横一列が完全に埋まる THEN Game_Engine SHALL その行を消去する
2. WHEN 行が消去される THEN Game_Engine SHALL 上の行を下に移動する
3. WHEN 複数行が同時に完成する THEN Game_Engine SHALL すべての完成行を消去する

### Requirement 5

**User Story:** プレイヤーとして、現在のゲーム状態を視覚的に確認できるようにしたい。そうすることで、適切な判断ができる。

#### Acceptance Criteria

1. THE Game_Display SHALL 現在のGame_Boardの状態を表示する
2. THE Game_Display SHALL 落下中のTetrominoを表示する
3. THE Game_Display SHALL 固定されたブロックを表示する
4. THE Game_Display SHALL 次に落下するTetrominoを表示する

### Requirement 6

**User Story:** プレイヤーとして、ゲームオーバー条件を理解できるようにしたい。そうすることで、ゲームの終了を認識できる。

#### Acceptance Criteria

1. WHEN 新しいTetrominoが生成位置に配置できない THEN Game_Engine SHALL ゲームオーバー状態にする
2. WHEN ゲームオーバーになる THEN Game_Display SHALL ゲームオーバーメッセージを表示する
3. WHEN ゲームオーバー状態になる THEN Game_Engine SHALL プレイヤー入力を無効にする

### Requirement 7

**User Story:** プレイヤーとして、7種類の標準的なTetrominoでプレイしたい。そうすることで、本格的なTetris体験ができる。

#### Acceptance Criteria

1. THE Game_Engine SHALL I、O、T、S、Z、J、Lの7種類のTetrominoを生成する
2. WHEN 新しいTetrominoを生成する THEN Game_Engine SHALL ランダムに7種類から選択する
3. THE Game_Engine SHALL 各Tetrominoの正しい形状と回転パターンを実装する