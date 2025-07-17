# Windows向けテトリスゲーム

これは、PythonとPygameで作成されたテトリスゲームです。

## 操作方法

-   **←キー**: テトリミノを左に移動
-   **→キー**: テトリミノを右に移動
-   **↓キー**: テトリミノを下に移動
-   **↑キー**: テトリミノを回転

## exeファイルの作成方法

このゲームは、PyInstallerを使用してWindows用の実行可能ファイル（`.exe`）に変換できます。

1.  **PythonとPygameのインストール**:
    -   Pythonがインストールされていない場合は、[公式サイト](https://www.python.org/)からダウンロードしてインストールしてください。
    -   次のコマンドを実行して、Pygameをインストールします。
        ```bash
        pip install pygame
        ```

2.  **PyInstallerのインストール**:
    -   次のコマンドを実行して、PyInstallerをインストールします。
        ```bash
        pip install pyinstaller
        ```

3.  **exeファイルのビルド**:
    -   ターミナルまたはコマンドプロンプトで`tetris.py`が保存されているディレクトリに移動します。
    -   次のコマンドを実行します。
        ```bash
        pyinstaller --onefile --windowed tetris.py
        ```

4.  **実行**:
    -   ビルドが完了すると、`dist`という名前のフォルダが作成されます。
    -   その中にある`tetris.exe`を実行すると、ゲームが起動します。