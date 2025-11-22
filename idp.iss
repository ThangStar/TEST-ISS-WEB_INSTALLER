; --- THÔNG TIN ỨNG DỤNG ---
#define MyAppName "T2Team"
#define MyAppVersion "1.0"
#define MyAppPublisher "ThangStar"
#define MyAppExeName "test.exe" 

; --- CẤU HÌNH DOWNLOAD ---
#define DownloadUrl "https://github.com/ThangStar/TEST-ISS-WEB_INSTALLER/releases/download/1/test.rar"
#define DownloadFileName "test.rar"

[Setup]
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputBaseFilename=WebInstaller_Native_RAR
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=admin

[Files]
; Nhúng 7za.exe để giải nén
Source: "7za.exe"; DestDir: "{tmp}"; Flags: deleteafterinstall

[Code]
var
  DownloadPage: TDownloadWizardPage;

procedure InitializeWizard;
begin
  // 1. Tạo trang tải xuống (Native của Inno Setup)
  DownloadPage := CreateDownloadPage(SetupMessage(msgWizardPreparing), 'Dang tai du lieu cai dat...', @OnDownloadProgress);
end;

function OnDownloadProgress(const Url, FileName: String; const Progress, ProgressMax: Int64): Boolean;
begin
  // Hàm này giữ cho thanh progress bar chạy mượt mà
  Result := True;
end;

function NextButtonClick(CurPageID: Integer): Boolean;
begin
  // 2. Kích hoạt tải xuống khi người dùng bấm Next ở trang "Ready to Install" (wpReady)
  if CurPageID = wpReady then begin
    DownloadPage.Clear;
    // Thêm file cần tải vào hàng đợi
    DownloadPage.Add('{#DownloadUrl}', '{#DownloadFileName}', '');
    
    DownloadPage.Show;
    try
      try
        // Bắt đầu tải
        DownloadPage.Download; 
        Result := True;
      except
        // Nếu lỗi mạng thì báo lỗi
        if DownloadPage.AbortedByUser then
          Log('Nguoi dung da huy tai xuong.')
        else
          SuppressbleMsgBox(GetExceptionMessage, mbCriticalError, MB_OK, IDOK);
        Result := False;
      end;
    finally
      DownloadPage.Hide;
    end;
  end else
    Result := True;
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  ResultCode: Integer;
begin
  // 3. Sau khi cài đặt xong (ssPostInstall) -> Giải nén file RAR
  if CurStep = ssPostInstall then 
  begin
    // Lấy file 7za từ temp
    ExtractTemporaryFile('7za.exe');
    
    WizardForm.StatusLabel.Caption := 'Dang giai nen du lieu...';

    // Giải nén file RAR vừa tải về (nằm trong {tmp})
    if Exec(ExpandConstant('{tmp}\7za.exe'), 
            'x "' + ExpandConstant('{tmp}\{#DownloadFileName}') + '" -o"' + ExpandConstant('{app}') + '" -y', 
            '', SW_HIDE, ewWaitUntilTerminated, ResultCode) then
    begin
      Log('Giai nen thanh cong.');
    end
    else begin
      MsgBox('Loi giai nen: ' + IntToStr(ResultCode), mbError, MB_OK);
    end;
  end;
end;