[void][System.Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms")

#▼コントロール定義
function ColorUnit($y, $text){
  #▼ラベル（影）
  $lbs = New-Object System.Windows.Forms.Label
  $lbs.Text = $text + "："
  $lbs.Top = $y + 1
  $lbs.Left = 1 + 1
  $lbs.Width = 23
  $lbs.Height = 20
  $lbs.TextAlign = [System.Drawing.ContentAlignment]::MiddleRight
  $lbs.ForeColor = [System.Drawing.Color]::Silver
  $mainForm.Controls.Add($lbs)
  
  #▼ラベル
  $lb = New-Object System.Windows.Forms.Label
  $lb.Parent = $lbs
  $lb.Text = $lbs.Text
  $lb.Top = - 1
  $lb.Left = - 1
  $lb.Width = $lbs.Width
  $lb.Height = $lbs.Height
  $lb.TextAlign = [System.Drawing.ContentAlignment]::MiddleRight
  $lb.ForeColor = [System.Drawing.Color]::Black
  $lb.BackColor = [System.Drawing.Color]::FromARGB(0, 255, 255, 255)
  $lbs.Controls.Add($lb)
  
  #▼スクロールバー
  $sb = New-Object System.Windows.Forms.HScrollBar
  $sb.Top = $y
  $sb.Left = 24
  $sb.Width = 156
  $sb.Height = 20
  $sb.Maximum = 255
  $sb.Minimum = 0
  $sb.LargeChange = 1
  $sb.SmallChange = 1
  $sb.Value = 127 # 初期値
  $sb.TabStop = $true
  $mainForm.Controls.Add($sb)
  
  #▼テキストボックス
  $tb = New-Object System.Windows.Forms.TextBox
  $tb.Top = $y
  $tb.Left = 180
  $tb.Width = 30
  $tb.MaxLength = 3
  $tb.ImeMode = [System.Windows.Forms.ImeMode]::Disable
  $tb.Text = $sb.Value
  $mainForm.Controls.Add($tb)
  
  #▼UpDownキー無効 (ScrollBar_KeyDown)
  $sb.Add_KeyDown({
    if(($_.KeyCode -eq [System.Windows.Forms.Keys]::Up) -or
       ($_.KeyCode -eq [System.Windows.Forms.Keys]::Down)){
      $_.Handled = $true
      $_.SuppressKeyPress = $true
    }
  })
  
  #▼UpDownキーで数値の増減を行う (TextBox_KeyDown)
  $tb.Add_KeyDown({
    if($_.KeyCode -eq [System.Windows.Forms.Keys]::Up){
      if([int]$this.Text -lt 255){
        $this.Text = [int]$this.Text + 1
        $_.Handled = $true
        $_.SuppressKeyPress = $true
      }
    }elseif($_.KeyCode -eq [System.Windows.Forms.Keys]::Down){
      if([int]$this.Text -gt 0){
        $this.Text = [int]$this.Text - 1
        $_.Handled = $true
        $_.SuppressKeyPress = $true
      }
    }
  })
  
  #▼ScrollBarとTextBoxの値連携
  $sb.Add_ValueChanged({
    $tb.Text = $sb.Value
  }.GetNewClosure())
  
  $tb.Add_TextChanged({
    RangeRGB $tb
    $sb.Value = $tb.Text
    ChangeColor
  }.GetNewClosure())
  
  #▼戻り値
  $obj = New-Object PSObject -Property @{
    Label = $lb
    ScrollBar = $sb
    TextBox = $tb
  }
  $obj | Add-Member ScriptProperty Value{
    [int]$this.TextBox.Text
  }
  return $obj
}

#▼TextBoxの内容を0-255へ置換
function RangeRGB($tb){
  # 数値 (10進数以外の文字を削除)
  $tb.Text = $tb.Text -replace "\D", ""
  
  # RGB値の範囲
  if($tb.Text -eq ""){
    $tb.Text = 0
  }elseif([int]$tb.Text -ge 256){
    $tb.Text = 255
  }
}

#▼母艦色変更
function ChangeColor(){
  $mainForm.BackColor = [System.Drawing.Color]::FromArgb(255, $r.Value, $g.Value, $b.Value)
  $mainForm.Text = "#{0:X2}{1:X2}{2:X2}" -f $r.Value, $g.Value, $b.Value
}

#▼母艦作成
$mainForm = New-Object System.Windows.Forms.Form
$mainForm.Width = 222 # 230
$mainForm.Height = 108 # 119
$mainForm.StartPosition = [System.Windows.Forms.FormStartPosition]::CenterScreen
$mainForm.MaximizeBox = $false
$mainForm.FormBorderStyle = [System.Windows.Forms.FormBorderStyle]::FixedDialog

#▼赤作成
$y = 5
$r = ColorUnit $y "赤"

#▼緑作成
$y += 25
$g = ColorUnit $y "緑"

#▼青作成
$y += 25
$b = ColorUnit $y "青"

#▼母艦浮上
ChangeColor
$mainForm.Show()
$mainForm.Activate()
[System.Windows.Forms.Application]::Run($mainForm)

exit

