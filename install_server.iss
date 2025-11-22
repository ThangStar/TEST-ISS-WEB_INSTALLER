; --- CẤU HÌNH ---
#define MyAppName "T2Tool"
#define MyAppVersion "1.0.0"
#define MyAppExeName "test.exe"
#define MyAppPublisher "THANG DEV"

; Link tải file RAR (đảm bảo test.exe nằm ở GỐC archive)
#define DownloadUrl "https://github.com/ThangStar/TEST-ISS-WEB_INSTALLER/releases/download/1/test.rar"
#define DownloadFileName "test.rar"

[Setup]
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppCopyright=Phát triển bởi {#MyAppPublisher}
DefaultDirName={pf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputBaseFilename=T2Tool-WebInstaller-1.0.0
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=admin

; --- GIAO DIỆN ĐẸP (bắt buộc có thư mục "assets" cùng .iss) ---
SetupIconFile=assets\logo.ico
WizardImageFile=assets\large3.bmp
WizardSmallImageFile=assets\small4.bmp
WizardImageStretch=No
WizardImageBackColor=clWhite

[Languages]
Name: "vietnamese"; MessagesFile: "compiler:Languages\Vietnamese.isl"

[Files]
; Nhúng UnRAR.exe (phải có file này cùng thư mục với .iss khi compile)
Source: "UnRAR.exe"; DestDir: "{tmp}"; Flags: deleteafterinstall
; Nhúng icon để tạo shortcut (dùng sau cài)
Source: "assets\logo.ico"; DestDir: "{tmp}"; Flags: dontcopy

[Icons]
; Icon nhóm và desktop — dùng icon từ assets (sẽ sao chép vào {app} sau giải nén)
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\assets\logo.ico"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; IconFilename: "{app}\assets\logo.ico"

[Registry]
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "{#MyAppName}"; ValueData: """{app}\{#MyAppExeName}"""; Tasks: autostartup

[Tasks]
Name: "desktopicon"; Description: "Tạo biểu tượng trên &màn hình"; GroupDescription: "Biểu tượng bổ sung:"; Flags: unchecked
Name: "autostartup"; Description: "&Khởi động cùng Windows"; GroupDescription: "Tùy chọn khởi động:"; Flags: unchecked

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Khởi chạy {#MyAppName}"; Flags: nowait postinstall skipifsilent

[Code]
var
  DownloadPage: TDownloadWizardPage;

function OnDownloadProgress(const Url, FileName: String; const Progress, ProgressMax: Int64): Boolean;
begin
  Result := True;
end;

procedure InitializeWizard;
begin
  DownloadPage := CreateDownloadPage(SetupMessage(msgWizardPreparing), 'Đang tải dữ liệu từ máy chủ...', @OnDownloadProgress);
end;

function NextButtonClick(CurPageID: Integer): Boolean;
begin
  if CurPageID = wpReady then
  begin
    DownloadPage.Clear;
    DownloadPage.Add('{#DownloadUrl}', '{#DownloadFileName}', '');
    DownloadPage.Show;
    try
      DownloadPage.Download;
      Result := True;
    except
      MsgBox('Lỗi tải file: ' + GetExceptionMessage, mbError, MB_OK);
      Result := False;
    end;
    DownloadPage.Hide;
  end
  else
    Result := True;
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  ResultCode: Integer;
  UnRarPath, RarPath, DestPath, ExePath: String;
begin
  if CurStep = ssPostInstall then
  begin
    UnRarPath := ExpandConstant('{tmp}\UnRAR.exe');
    RarPath := ExpandConstant('{tmp}\{#DownloadFileName}');
    DestPath := ExpandConstant('{app}');
    ExePath := ExpandConstant('{app}\{#MyAppExeName}');

    WizardForm.StatusLabel.Caption := 'Đang giải nén ứng dụng...';

    // Kiểm tra UnRAR.exe
    if not FileExists(UnRarPath) then
    begin
      MsgBox('Lỗi: UnRAR.exe bị thiếu!', mbError, MB_OK);
      Exit;
    end;

    // Kiểm tra file RAR
    if not FileExists(RarPath) then
    begin
      MsgBox('Lỗi: Không tìm thấy file RAR đã tải!', mbError, MB_OK);
      Exit;
    end;

    // Tạo thư mục đích
    if not DirExists(DestPath) then
      ForceDirectories(DestPath);

    // Giải nén RAR vào {app}
    if Exec(UnRarPath,
            'x -y -op"' + DestPath + '" "' + RarPath + '"',
            '',
            SW_HIDE, ewWaitUntilTerminated, ResultCode) then
    begin
      if ResultCode <> 0 then
      begin
        MsgBox('Lỗi giải nén (mã: ' + IntToStr(ResultCode) + '). Vui lòng kiểm tra file RAR.', mbError, MB_OK);
        Exit;
      end;
    end
    else
    begin
      MsgBox('Không thể chạy UnRAR.exe!', mbError, MB_OK);
      Exit;
    end;

    // SAO CHÉP ICON VÀO {app}\assets (để shortcut dùng được)
    if not DirExists(ExpandConstant('{app}\assets')) then
      ForceDirectories(ExpandConstant('{app}\assets'));
    
    ExtractTemporaryFile('logo.ico');
    if not FileCopy(ExpandConstant('{tmp}\logo.ico'), ExpandConstant('{app}\assets\logo.ico'), False) then
    begin
      Log('Cảnh báo: Không sao chép được icon vào thư mục assets.');
    end;

    // Kiểm tra file chính
    if not FileExists(ExePath) then
    begin
      MsgBox('Lỗi nghiêm trọng: Không tìm thấy file chính "' + ExePath + '" sau giải nén!' + #13#10 +
             'Vui lòng đảm bảo file RAR có "test.exe" ở GỐC archive.', mbError, MB_OK);
      Exit;
    end;

    Log('Cài đặt hoàn tất thành công.');
  end;
end;