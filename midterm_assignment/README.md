# MIDTERM PROJECT

이 프로젝트는 파노라마 생성 및 특수 효과 적용 프로그램을 포함합니다. 각각의 프로그램은 별도로 실행할 수 있으며, 필요한 의존성과 설정 파일들이 개별적으로 작성되어 있습니다.

## 프로젝트 구조
- **build**
- **dist**: 실행파일(.exe)가 저장되어 있는 디렉터리

- **pano_img**: 파노라마 이미지를 저장하는 디렉터리

- **pano_project**: make_panorama.py의 세부정보 디렉터리
  - **pyproject.toml**: 파노라마 프로젝트 의존성 및 빌드 정보
  - **README.md**: 파노라마 프로젝트에 대한 설명
  - **requirements.txt**: 파노라마 프로젝트에 필요한 Python 라이브러리

- **se_img**: 특수 효과 이미지를 저장하는 디렉터리

- **se_project**: make_specialeffect.py의 세부정보 디렉터리
  - **pyproject.toml**: 특수효과 프로젝트 의존성 및 빌드 정보
  - **README.md**: 특수효과 프로젝트에 대한 설명
  - **requirements.txt**: 특수효과 프로젝트에 필요한 Python 라이브러리

- **src**: 소스 코드가 포함된 디렉터리
  - `make_panorama.py`: 파노라마 생성 프로그램
  - `make_specialeffect.py`: 특수 효과 적용 프로그램

- ****
- **make_panorama.spec**
- **make_specialeffect.spec**

각 프로그램에 대한 세부 정보는 `pano_project` 그리고 `se_project` 디렉터리안에 있는 각각의 README 파일을 참조할 수 있습니다.

### 실행파일
각 프로그램에 대한 실행은 `dist` 디렉터리 안에 있는 .exe파일로 실행할 수 있습니다.
- **make_panorama.exe**: 콘솔 창이 함께 나타남(--onefile)
- **make_specialeffect.exe**: 콘솔 창 없이 GUI 애플리케이션으로 실행(--onefile --windowed)