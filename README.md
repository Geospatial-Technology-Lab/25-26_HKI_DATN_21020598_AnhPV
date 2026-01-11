# iHydroSlide3D v1.1

## Giới thiệu

iHydroSlide3D v1.1 là phần mềm mã nguồn mở, song song hóa và mô-đun hóa để mô phỏng và dự báo các quá trình thủy văn khu vực và sạt lở đất. Phần mềm bao gồm các mô-đun chính:

- **(i)** Mô hình thủy văn phân tán (CREST)
- **(ii)** Mô hình ổn định mái dốc 3D khu vực
- **(iii)** Phương pháp hạ thấp độ phân giải độ ẩm đất (SMD)

## Đặc điểm chính

- Ứng dụng đa nền tảng
- Tính toán song song trong cả mô-đun thủy văn và mô-đun ổn định mái dốc
- Nén HDF5 để tiết kiệm thời gian I/O và lưu trữ
- Trực quan hóa hậu xử lý cho hình ảnh và video

## Yêu cầu phần mềm/môi trường

- CMake ≥ 3.23
- Trình biên dịch Fortran: GNU ≥ 11.2 hoặc Intel oneAPI (khuyến nghị GNU)
- OpenMP ≥ 4.5
- HDF5 ≥ 1.10.*
- Python ≥ 3.8

## Yêu cầu phần cứng

- RAM ≥ 3 GB
- Số lõi CPU ≥ 2

iHydroSlide3D có thể chạy trên hầu hết các thiết bị máy tính hiện tại, từ máy tính cá nhân đến máy tính hiệu năng cao (HPC).

---

## Hướng dẫn cài đặt

### Bước 1: Tải mã nguồn

Mở terminal và chạy lệnh sau:

```bash
git clone https://github.com/Geospatial-Technology-Lab/25-26_HKI_DATN_21020598_AnhPV.git
```

### Bước 2: Thay đổi các đường dẫn

Chỉnh sửa file `CMakeLists.txt`


### Bước 3: Biên dịch phần mềm

Vào thư mục "Build":

```bash
cd Build
```

Cấu hình CMake:

```bash
cmake ..
```

Biên dịch:

```bash
make
```

Nếu thành công, bạn sẽ nhận được file thực thi: `iHydroSlide3D`

---

## Cấu trúc thư mục

```
📦iHydroSlide3D_v1.0
 ┣ 📂Build                    (Thư mục lưu trữ file cấu hình CMake)
 ┣ 📂DownscalingBasicData     (Dữ liệu đầu vào cho mô-đun hạ thấp độ ẩm đất)
 ┃ ┣ 📜TWI_coarse.asc         (Chỉ số ẩm địa hình độ phân giải thô)
 ┃ ┣ 📜TWI_fine.asc           (Chỉ số ẩm địa hình độ phân giải mịn)
 ┃ ┣ 📜aspect_coarse.asc      (Góc hướng địa lý độ phân giải thô)
 ┃ ┣ 📜curvature_coarse.asc   (Độ cong độ phân giải thô)
 ┃ ┗ 📜curvature_fine.asc     (Độ cong độ phân giải mịn)
 ┣ 📂HydroBasics              (Dữ liệu đầu vào cho mô-đun thủy văn)
 ┃ ┣ 📜DEM.asc                (Mô hình số độ cao)
 ┃ ┣ 📜FAC.asc                (Tích lũy dòng chảy)
 ┃ ┣ 📜FDR.asc                (Hướng dòng chảy)
 ┃ ┣ 📜Mask.asc               (Các pixel tính toán trong lưu vực)
 ┃ ┗ 📜Stream.asc             (Các pixel kênh sông)
 ┣ 📂ICS                      (Thiết lập điều kiện ban đầu)
 ┃ ┗ 📋InitialConditions.txt
 ┣ 📂LandslideBasics          (Dữ liệu đầu vào cho mô-đun sạt lở)
 ┃ ┣ 📜DEM_fine.asc           (DEM độ phân giải mịn)
 ┃ ┣ 📜Soil.asc               (Bản đồ cấu trúc đất)
 ┃ ┣ 📜aspect_fine.asc        (Góc hướng độ phân giải mịn)
 ┃ ┣ 📜mask_fine.asc          (Bản đồ mask độ phân giải mịn)
 ┃ ┗ 📜slope_fine.asc         (Góc dốc độ phân giải mịn)
 ┣ 📂OBS                      (Quan trắc thực địa để hiệu chỉnh)
 ┣ 📂PETs                     (Dữ liệu bốc hơi theo giờ)
 ┣ 📂Params                   (Các tham số mô hình)
 ┃ ┣ 📜IM.asc                 (Tỷ lệ diện tích không thấm)
 ┃ ┣ 📜Ksat.asc               (Hệ số thấm bão hòa của đất)
 ┃ ┣ 📋Parameters_hydro.txt   (Tham số mô-đun thủy văn)
 ┃ ┣ 📋Parameters_land.txt    (Tham số mô-đun sạt lở)
 ┃ ┣ 📋Parameters_parallel.txt (Thiết lập tính toán song song)
 ┃ ┗ 📜WM.asc                 (Dung lượng chứa nước của đất)
 ┣ 📂Rains                    (Dữ liệu mưa theo giờ)
 ┣ 📂Results                  (Lưu trữ kết quả mô phỏng)
 ┣ 📂States                   (Biến trung gian cho khởi động ấm)
 ┣ 📂Visualization            (Dữ liệu và mã trực quan hóa)
 ┣ 📂include                  (File biên dịch .mod)
 ┣ 📂logs                     (Nhật ký mô phỏng)
 ┣ 📂src                      (Mã nguồn Fortran nếu cần chỉnh source code thì chỉnh trong này xong build lại)
 ┣ 📋CMakeLists.txt           (File CMake)
 ┗ 📋Control.Project          (Thông tin cơ bản cho mô phỏng)
```

---

## Chạy mô hình

### Thiết lập cơ bản trong Control.Project tùy chỉnh theo vùng nghiên cứu

#### 1. Thông tin cơ bản mô-đun thủy văn và ổn định mái dốc

```python
# Bản đồ thủy văn
NCols_Hydro     = 598    # Số cột
NRows_Hydro     = 650    # Số hàng
XLLCorner_Hydro = 108.335815
YLLCorner_Hydro = 32.654663
CellSize_Hydro  = 0.000833	

# Bản đồ sạt lở
NCols_Land      = 3481   # Số cột
NRows_Land      = 3891   # Số hàng
XLLCorner_Land  = 108.354919
YLLCorner_Land  = 32.674500
CellSize_Land   = 0.000125	

NoData_value    = -9999
```

#### 2. Hệ tọa độ

```python
# GCS: Hệ tọa độ địa lý
# PCS: Hệ tọa độ chiếu
CoordinateSystem = GCS 
```

#### 3. Thông tin thời gian mô phỏng

```python
TimeMark    = h              # y(năm);m(tháng);d(ngày);h(giờ);u(phút);s(giây)
TimeStep    = 1
StartDate   = 2012062700   
LoadState   = no             # Chuyển "yes" để khởi động ấm
WarmupDate  = 2012070201     # Ngày bắt đầu khởi động ấm
EndDate     = 2012062704  
SaveState   = no             # Lưu biến trung gian cho khởi động ấm tiếp theo
```

#### 4. Kiểu chạy mô hình

```python
RunStyle    = simu           # simu, cali_SCEUA
ModelCore   = HydroSlide3D   # Hydro (chỉ thủy văn), HydroSlide3D
RoutingType = CLR            # JLR (mặc định), CLR
```
Nếu chỉ chạy Hydro thì chỉ cần chuẩn bị data trong Hydrobasic và Param (ICS nếu có data)

### Chạy iHydroSlide3D

```bash
./iHydroSlide3D
```

---

## Các tham số mô hình (đừng sửa thông số nếu không chắc chắn)

| Tham số       | Mô tả                                           | Đơn vị          | Phạm vi     |
| :------------ | :---------------------------------------------- | --------------- | ----------- |
| $K_{sat}$     | Hệ số thấm bão hòa của đất                      | mm/h            | /           |
| $WM$          | Dung lượng chứa nước của đất                    | mm              | /           |
| $B$           | Số mũ của đường cong thấm biến đổi              | -               | [0.05, 1.5] |
| $IM$          | Tỷ lệ diện tích không thấm                      | -               | /           |
| $coeM$        | Hệ số vận tốc dòng chảy mặt                     | -               | [1, 150]    |
| $expM$        | Số mũ tốc độ dòng chảy mặt                      | -               | [0.1, 0.55] |
| $coeR$        | Tỷ lệ tốc độ dòng kênh/mặt                      | -               | [1, 3]      |
| $coeS$        | Tỷ lệ tốc độ dòng ngầm/mặt                      | -               | [0.01, 1]   |
| $c_s$         | Lực dính của đất                                | kPa             | /           |
| $\gamma_{s}$  | Trọng lượng riêng đất khô                       | kN/m³           | /           |
| $\varphi$     | Góc ma sát trong                                | °               | /           |

---

## Kết quả đầu ra

Chuyển sang "yes" trong `Control.Project` để xác nhận đầu ra:

- **GOVar_Rain**: Lượng mưa đầu vào (mm/h)
- **GOVar_SM**: Độ ẩm đất (%)
- **GOVar_R**: Lưu lượng mô phỏng của từng ô lưới (m³/s)
- **GOVar_FS3D**: Hệ số an toàn theo mô hình 3D
- **GOVar_PF**: Xác suất xảy ra sạt lở
- **GOVar_FVolume**: Thể tích sạt lở (m³)
- **GOVar_FArea**: Diện tích bề mặt sạt lở (m²)

---

## Trực quan hóa

Vào thư mục "Visualization" và chạy:

```bash
python Plot_all.py
```

nếu muốn xuất output ra dạng tif thì chạy 

```bash
python ExportTIF.py
```

---

## Liên hệ

Tham khảo để biết thêm chi tiết
Guoding Chen: [guoding.chen94@gmail.com](mailto:guoding.chen94@gmail.com)
https://gmd.copernicus.org/articles/16/2915/2023/
https://github.com/GuodingChen/iHydroSlide3D


 		



