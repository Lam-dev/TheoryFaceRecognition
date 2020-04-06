import sqlite3

duongDanTepSqlite = "../Database/Database"

class LayDuLieuTrongDataBase:
    def __init__(self, duongDanDataBase, tenBang):
        #self.duongDanDataBase = duongDanDataBase; 
        # print("aaa", duongDanDataBase)
        self.CSDL = sqlite3.connect(duongDanDataBase)

        self.tenBang = tenBang

    """
    lay danh sach du lieu
    """
    def capNhatTruong(self, truongTuple, giaTriTuple, oDau):
        try:
            cursor = self.CSDL.cursor()
            sql = 'update `' + self.tenBang + '` set '
            for i in range(0,truongTuple.__len__()):
                if(i < truongTuple.__len__() - 1):
                    sql += '`%s` = "%s", ' % (truongTuple[i].__str__(), giaTriTuple[i].__str__())
                else:
                    sql += '`%s` = "%s" ' % (truongTuple[i].__str__(), giaTriTuple[i].__str__())
            sql += 'where %s' % (oDau)
            #print("sql = ", sql)
            cursor.execute(sql)
            self.CSDL.commit()
        except:
            pass
    """
    Lay du lieu o mot hoac mot so truong
    """
    def LayDuLieuTaiTruong(self, truongTuple, oDau): #moi chi dung de lay du lieu (ID_Thi_Sinh, Cam_Bien_van_tay)
        cursor = self.CSDL.cursor()
        select = ""
        for i in range(0,truongTuple.__len__()):
            if(i < truongTuple.__len__() - 1):
                select += '`%s`,'%(truongTuple[i])
            else:
                select += '`%s`'%(truongTuple[0])
        sql = 'SELECT %s FROM `%s` WHERE %s' %(select, self.tenBang, oDau)   
        cursor.execute(sql)
        results = cursor.fetchall()
        return results
    """
    Lay danh sach hoc vien
    """
    def layDanhSach(self, where):
        cursor = self.CSDL.cursor()
        sql = 'SELECT  * FROM `'+ self.tenBang + '` WHERE ' + where
        cursor.execute(sql)
        results = cursor.fetchall()
        if(self.tenBang == "ThongTinThiSinh"):
            # try:
            #     IDkhoaHoc  = where.split("=")[1]
            #     khoaHoc = KhoaThiRepository().layDanhSach( " IDKhoaThi = %s "%(str(IDkhoaHoc)))
            #     tenKhoaHoc = khoaHoc[0].TenKhoaHoc
            # except:
            #     tenKhoaHoc = ""
            listThiSinh = [];
            for i in range(0, len(results)):
                thiSinh = ThongTinThiSinh()
                thiSinh.ID = results[i][0]
                thiSinh.IDKhoaHoc = results[i][1]
                thiSinh.SBD = results[i][2]
                thiSinh.HoVaTen = results[i][3]
                thiSinh.NgaySinh = results[i][4]
                thiSinh.SoCMTND = results[i][5]
                thiSinh.NgayDangKy = results[i][6]
                thiSinh.AnhDangKy = results[i][7]
                try:
                    tenKhoaHoc = KhoaThiRepository().layDanhSach( " IDKhoaThi = %s "%(str(thiSinh.IDKhoaHoc)))[0].TenKhoaThi
                    thiSinh.TenKhoaHoc = tenKhoaHoc
                except:
                    pass
                if((results[i][8] != None) & (results[i][11] != "")):
                    lstDSdacTrung = results[i][8].split(';')
                    for k in range (0, len(lstDSdacTrung)):
                        lstDacTrung = lstDSdacTrung[k].split(',')
                        thiSinh.NhanDienKhuonMat.append([])
                        if(len(lstDacTrung) == 128):
                            for j in range (0,128):
                                thiSinh.NhanDienKhuonMat[k].append(j)
                                thiSinh.NhanDienKhuonMat[k][j] =  float(lstDacTrung[j])
                
                if((results[i][11] != None) & (results[i][11] != "")):
                    lstDSdacTrung = results[i][11].split(';')
                    for k in range (0, len(lstDSdacTrung)):
                        lstDacTrung = lstDSdacTrung[k].split(',')
                        thiSinh.NhanDienKhuonMatThem.append([])
                        if(len(lstDacTrung) == 128):
                            for j in range (0,128):
                                thiSinh.NhanDienKhuonMatThem[k].append(j)
                                thiSinh.NhanDienKhuonMatThem[k][j] =  float(lstDacTrung[j])
                else:
                    thiSinh.NhanDienKhuonMatThem = []

                listThiSinh.append(thiSinh)
                thiSinh.MaDK = results[i][10]
                del thiSinh   
            return listThiSinh

        elif(self.tenBang == "LichSuDiemDanh"):
            lstLichSu = []
            for i in range(0, len(results)):
                lichSu = ThongTinLichSuDiemDanh()
                lichSu.IDThiSinh = results[i][0]
                lichSu.ThoiGian = results[i][1]
                lichSu.Anh = results[i][2]
                lichSu.KhuonMatHayVanTay = results[i][3]
                lstLichSu.append(lichSu)
                del lichSu
            return lstLichSu

        elif(self.tenBang == "ThongTinKhoaThi"):
            lstKhoaThi = []
            for i in range(0, len(results)):
                khoaThi = ThongTinKhoaThi()
                khoaThi.IDKhoaThi = results[i][0]
                khoaThi.NgayTao = results[i][1]
                khoaThi.TenKhoaThi = results[i][2]
                khoaThi.DuongDanLuuAnh = results[i][3]
                lstKhoaThi.append(khoaThi)
                del khoaThi
            return lstKhoaThi

        elif(self.tenBang == "AnhXaIDvaVanTay"):
            lstIDvaVanTay = []
            for i in range(0, len(results)):
                idVaVanTay = AnhXaIDvaVanTay()
                idVaVanTay.IDThiSinh = results[i][0]
                idVaVanTay.ViTriVanTay = results[i][1]
                idVaVanTay.DacTrungVanTay = results[i][2]
                idVaVanTay.AnhVanTay = results[i][3]
                lstIDvaVanTay.append(idVaVanTay)
                del idVaVanTay
            return lstIDvaVanTay

        elif(self.tenBang == "TaiKhoanQuanLy"):
            lstTaiKhoanQuanLy = []
            for i in range(0, len(results)):
                taiKhoanVaMatKhau = ThongTinTaiKhoanQuanLy()
                taiKhoanVaMatKhau.IDtaiKhoan = results[i][0]
                taiKhoanVaMatKhau.TaiKhoan = results[i][1]
                taiKhoanVaMatKhau.MatKhau = results[i][2]
                lstTaiKhoanQuanLy.append(taiKhoanVaMatKhau)
                del taiKhoanVaMatKhau
            return lstTaiKhoanQuanLy

        elif(self.tenBang == "HocVienTuongUngTaiKhoanQuanLy"):
            lstHocVienTuongUngTaiKhoan = []
            for i in range(0, len(results)):
                hocVienVaTaiKhoanQuanLy = HocVienTuongUngTaiKhoanQuanLy()
                hocVienVaTaiKhoanQuanLy.IDthiSinh = results[i][0]
                hocVienVaTaiKhoanQuanLy.IDtaiKhoan = results[i][1]
                lstHocVienTuongUngTaiKhoan.append(hocVienVaTaiKhoanQuanLy)
                del lstHocVienTuongUngTaiKhoan
            return lstHocVienTuongUngTaiKhoan
        elif(self.tenBang == ""):


    def ghiDuLieu(self, thongTin):
        try:
            cursor = self.CSDL.cursor()
            if(self.tenBang == "ThongTinThiSinh"):
                sql = 'INSERT INTO `ThongTinThiSinh`(`ID`, `IDKhoaThi`, `SBD`, `HoVaTen`, `NgaySinh`, `SoCMTND`, `NgayDangKy`, `AnhDangKy`, `NhanDienKhuonMat`, `NhanDienVanTay`, `MaDK`) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", ?, "%s", "%s", "%s")'%(thongTin.ID, thongTin.IDKhoaThi, thongTin.SBD, thongTin.HoVaTen, thongTin.NgaySinh, thongTin.SoCMTND, thongTin.NgayDangKy, thongTin.NhanDienKhuonMatStr, thongTin.NhanDienVanTay, thongTin.MaDK)
                print(cursor.execute(sql, (sqlite3.Binary(thongTin.AnhDangKy), )))
                self.CSDL.commit()

            elif(self.tenBang == "LichSuDiemDanh"):
                sql = 'INSERT INTO `LichSuDiemDanh`(`IDThiSinh`, `ThoiGian`, `KhuonMatHayVanTay`, `Anh`) VALUES ("%s", "%s","%s", ?)'%(thongTin.IDThiSinh, thongTin.ThoiGian, thongTin.KhuonMatHayVanTay)
                print(cursor.execute(sql, (sqlite3.Binary(thongTin.Anh), )))
                self.CSDL.commit()

            elif(self.tenBang == "ThongTinKhoaThi"):
                sql = 'INSERT INTO `ThongTinKhoaThi`(`IDKhoaThi`,`NgayTao`, `TenKhoaThi`, `ThuMucLuuAnh`) VALUES ("%s", "%s", "%s", "%s")'%(str(thongTin.IDKhoaThi) ,thongTin.NgayTao, thongTin.TenKhoaThi, thongTin.DuongDanLuuAnh)
                key = cursor.execute(sql).lastrowid
                self.CSDL.commit()
                return key

            elif(self.tenBang == "AnhXaIDvaVanTay"):
                sql = 'INSERT INTO `AnhXaIDvaVanTay`(`IDThiSinh`, `ViTriVanTay`, `DacTrungVanTay`) VALUES ("%s", "%s", "%s")'%(thongTin.IDThiSinh, thongTin.ViTriVanTay, thongTin.DacTrungVanTay)
                cursor.execute(sql)
                self.CSDL.commit()

            elif(self.tenBang == "TaiKhoanQuanLy"):
                sql = 'INSERT INTO `TaiKhoanQuanLy`(`TaiKhoan`, `MatKhau`) VALUES ("%s", "%s")'%(thongTin.TaiKhoan, thongTin.MatKhau)
                cursor.execute(sql)
                self.CSDL.commit()

            elif(self.tenBang == "HocVienTuongUngTaiKhoanQuanLy"):
                sql = 'INSERT INTO `HocVienTuongUngTaiKhoanQuanLy`(`IDThiSinh`, `IDTaiKhoanQuanLy`) VALUES ("%s", "%s")'%(thongTin.IDthiSinh, thongTin.IDtaiKhoan)
                cursor.execute(sql)
                self.CSDL.commit()
            
        except sqlite3.Error as e:
            print(e)
    
    def xoaBanGhi(self, dieuKien):
        try:
            cursor = self.CSDL.cursor()
            sql = 'DELETE FROM `%s` WHERE %s'%(self.tenBang ,dieuKien)
            print(cursor.execute(sql))
            self.CSDL.commit()
            cursor.close()
        except sqlite3.Error as e:
            pass

class ThiSinhRepository(LayDuLieuTrongDataBase):
    def __init__(self, duongDanTepSqlite = "../Database/Database"): 
        super().__init__(duongDanTepSqlite, "ThongTinThiSinh")
        return

class LichSuRepository(LayDuLieuTrongDataBase):
    def __init__(self, duongDanTepSqlite = "../Database/Database"): 
        super().__init__(duongDanTepSqlite, "LichSuDiemDanh")
        return

class KhoaThiRepository(LayDuLieuTrongDataBase):
    def __init__(self, duongDanTepSqlite = "../Database/Database"):
        super().__init__(duongDanTepSqlite, "ThongTinKhoaThi")
        return

class IDvaVanTayRepository(LayDuLieuTrongDataBase):
    def __init__(self, duongDanTepSqlite = "../Database/Database"):
        super().__init__(duongDanTepSqlite, "AnhXaIDvaVanTay")
        return

class TaiKhoanQuanLyRepository(LayDuLieuTrongDataBase):
    def __init__(self, duongDanTepSqlite = "../Database/Database"):
        super().__init__(duongDanTepSqlite, "TaiKhoanQuanLy")
        return

class DanhSachThiSinhTuongUngTaiKhoanRepository(LayDuLieuTrongDataBase):
    def __init__(self, duongDanTepSqlite = "../Database/Database"):
        super().__init__(duongDanTepSqlite, "HocVienTuongUngTaiKhoanQuanLy")
        return

class ThongTinLichSuDiemDanh:
    def __init__(self):
        self.IDThiSinh = ""
        self.ThoiGian = ""
        self.Anh = ""
        self.KhuonMatHayVanTay= ""

class ThongTinKhoaThi:
    def __init__(self):
        self.IDKhoaThi = ""
        self.NgayTao = ""
        self.TenKhoaThi = ""
        self.DuongDanLuuAnh = ""

class ThongTinTaiKhoanQuanLy:
    def __init__(self):
        self.IDtaiKhoan = ""
        self.TaiKhoan = ""
        self.MatKhau = ""
        self.IDtrongBangThiSinh = ""

class AnhXaIDvaVanTay:
    def __init__(self):
        self.IDThiSinh = ""
        self.ViTriVanTay = ""
        self.DacTrungVanTay = ""
        self.AnhVanTay = ""

class ThongTinThiSinh:
    def __init__(self):
        self.HoVaTen = ""
        self.SBD = "" 
        self.NgaySinh = ""
        self.SoCMTND = ""
        self.NhanDienKhuonMat = []
        self.NhanDienKhuonMatStr = ""
        self.NhanDienVanTay = ""
        self.ID = ""
        self.MaDK = ""
        self.IDKhoaThi = ""
        self.TenKhoaHoc = ""
        self.NgayDangKy = ""
        self.AnhDangKy = ""
        self.NhanDienKhuonMatThem = []

class HocVienTuongUngTaiKhoanQuanLy:
    def __init__(self):
        self.IDthiSinh = ""
        self.IDtaiKhoan = ""

class GetDataFromDatabase():
    def __init__(self):
        pass

    def GetListStudent(self):
        studentRepo = ThiSinhRepository()
        lstStudent = studentRepo.layDanhSach(" 1 = 1 ")
        return lstStudent

# x = GetDataFromDatabase()
# y = x.GetListStudent()
# pass
