# -*- coding: utf-8 -*-
"""Formas de avisar: Windows (notificação + som)."""
import html
import subprocess
import time


def windows(titulo, texto):
    t = html.escape(titulo).replace("'", "''")
    x = html.escape(texto).replace("'", "''")
    ps = (
        "[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType=WindowsRuntime] > $null;"
        "[Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType=WindowsRuntime] > $null;"
        "$x = New-Object Windows.Data.Xml.Dom.XmlDocument;"
        "$x.LoadXml('<toast scenario=\"reminder\"><visual><binding template=\"ToastGeneric\"><text>%s</text><text>%s</text></binding></visual>"
        "<audio src=\"ms-winsoundevent:Notification.Looping.Alarm\" loop=\"false\"/></toast>');"
        "$app = '{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\\WindowsPowerShell\\v1.0\\powershell.exe';"
        "[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier($app).Show("
        "(New-Object Windows.UI.Notifications.ToastNotification $x))"
    ) % (t, x)
    try:
        subprocess.Popen(["powershell", "-NoProfile", "-Command", ps],
                         creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    except Exception as e:
        print("  (falha na notificação do Windows: %s)" % e)


def bipe(prioridade=False):
    try:
        import winsound
        for _ in range(4 if prioridade else 2):
            winsound.Beep(1800 if prioridade else 1200, 250)
            time.sleep(0.08)
    except Exception:
        pass
