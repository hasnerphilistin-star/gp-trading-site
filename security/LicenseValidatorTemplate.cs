using System;
using System.IO;
using System.Security.Cryptography;
using System.Text;
using System.Windows.Media;
using NinjaTrader.Gui;
using NinjaTrader.NinjaScript;

namespace GpTrading.Licensing
{
    public enum LicenseStatus
    {
        Valid,
        Trial,
        Expired,
        Invalid
    }

    public static class LicenseValidator
    {
        private const string PRODUCT_ID = "__PRODUCT_ID__";
        private const string LICENSES_SUBDIR = @"bin\Custom\Licenses";
        private const string TRIAL_FILE = "__PRODUCT_ID__.trial";
        private const int TRIAL_DAYS = 3;
        private const string KEY_PREFIX = "GPTR-";
        private const string LOCK_TAG = "GP_Lock";

        private static string _cachedAccountId;
        private static string _cachedSecret;

        public static LicenseStatus Validate(out int remainingDays)
        {
            remainingDays = 0;
            try
            {
                string licensesPath = GetLicensesPath();
                if (licensesPath == null) return LicenseStatus.Invalid;

                string licFile = Path.Combine(licensesPath, PRODUCT_ID + ".lic");
                if (File.Exists(licFile))
                {
                    string storedKey = File.ReadAllText(licFile)?.Trim();
                    if (!string.IsNullOrEmpty(storedKey) && ValidateKey(storedKey))
                        return LicenseStatus.Valid;
                }

                return HandleTrial(licensesPath, out remainingDays);
            }
            catch { return LicenseStatus.Invalid; }
        }

        public static void RemoveLockScreen(NinjaScriptBase owner)
        {
            try { Draw.RemoveDrawObject(owner, LOCK_TAG); }
            catch { }
        }

        public static void DrawTrialBanner(NinjaScriptBase owner, int daysLeft)
        {
            try
            {
                Draw.RemoveDrawObject(owner, LOCK_TAG);
                Draw.TextFixed(
                    owner,
                    LOCK_TAG,
                    "GP TRADING — Prueba: " + daysLeft + " día" + (daysLeft > 1 ? "s" : "") + " restante" + (daysLeft > 1 ? "s" : ""),
                    TextPosition.TopRight,
                    Brushes.Gold,
                    new SolidColorBrush(Color.FromRgb(10, 10, 10)),
                    11
                );
            }
            catch { }
        }

        public static void DrawLockScreen(NinjaScriptBase owner)
        {
            try
            {
                Draw.RemoveDrawObject(owner, LOCK_TAG);

                string message = ""
                    + "═══ GP TRADING ═══\n\n"
                    + "HERRAMIENTA SIN LICENCIA\n\n"
                    + "Comunícate con nosotros para\n"
                    + "adquirir tu licencia oficial:\n\n"
                    + "✉  gptradingacademy@proton.me\n"
                    + "💬  discord.com/invite/umVY4BQnKE\n"
                    + "📷  @gptradingfx\n"
                    + "📺  @GPTradingFX\n"
                    + "✈  t.me/gptradinggratis\n\n"
                    + "GP Trading Academy\n"
                    + "gptradingfx.pages.dev";

                Draw.TextFixed(
                    owner,
                    LOCK_TAG,
                    message,
                    TextPosition.Center,
                    Brushes.White,
                    new SolidColorBrush(Color.FromRgb(10, 10, 10)),
                    12
                );
            }
            catch { }
        }

        private static LicenseStatus HandleTrial(string licensesPath, out int remainingDays)
        {
            remainingDays = 0;
            string trialFile = Path.Combine(licensesPath, TRIAL_FILE);

            if (!File.Exists(trialFile))
            {
                File.WriteAllText(trialFile, DateTime.UtcNow.ToString("o"));
                remainingDays = TRIAL_DAYS;
                return LicenseStatus.Trial;
            }

            string dateStr = File.ReadAllText(trialFile)?.Trim();
            if (DateTime.TryParse(dateStr, out DateTime trialStart))
            {
                int elapsed = (int)(DateTime.UtcNow - trialStart).TotalDays;
                remainingDays = Math.Max(0, TRIAL_DAYS - elapsed);
                return elapsed >= TRIAL_DAYS ? LicenseStatus.Expired : LicenseStatus.Trial;
            }

            remainingDays = TRIAL_DAYS;
            return LicenseStatus.Trial;
        }

        private static bool ValidateKey(string licenseKey)
        {
            if (string.IsNullOrEmpty(licenseKey) || !licenseKey.StartsWith(KEY_PREFIX))
                return false;

            string accountId = GetAccountId();
            if (string.IsNullOrEmpty(accountId)) return false;

            return licenseKey == GenerateKey(accountId);
        }

        internal static string GenerateKey(string accountId)
        {
            string secret = GetSecret();
            string data = accountId + "|" + PRODUCT_ID + "|" + secret;

            using (SHA256 sha256 = SHA256.Create())
            {
                byte[] hash = sha256.ComputeHash(Encoding.UTF8.GetBytes(data));
                string hex = BitConverter.ToString(hash).Replace("-", "").ToUpperInvariant();
                return KEY_PREFIX
                    + hex.Substring(0, 5) + "-"
                    + hex.Substring(5, 5) + "-"
                    + hex.Substring(10, 5) + "-"
                    + hex.Substring(15, 5);
            }
        }

        private static string GetSecret()
        {
            if (!string.IsNullOrEmpty(_cachedSecret)) return _cachedSecret;
            _cachedSecret = Environment.GetEnvironmentVariable("GPT_LICENSE_SECRET");
            if (string.IsNullOrEmpty(_cachedSecret))
                _cachedSecret = "__MASTER_SECRET__";
            return _cachedSecret;
        }

        private static string GetAccountId()
        {
            if (!string.IsNullOrEmpty(_cachedAccountId)) return _cachedAccountId;

            try
            {
                string ntPath = GetNinjaTraderPath();
                if (ntPath == null) return null;

                string licPath = Path.Combine(ntPath, @"bin\Custom\Licenses.txt");

                if (File.Exists(licPath))
                {
                    string content = File.ReadAllText(licPath);
                    var match = System.Text.RegularExpressions.Regex.Match(
                        content,
                        @"AccountId\s*=\s*""([^""]+)"""
                    );
                    if (match.Success)
                    {
                        _cachedAccountId = match.Groups[1].Value;
                        return _cachedAccountId;
                    }
                }
            }
            catch { }

            _cachedAccountId = "unknown-" + Environment.UserName;
            return _cachedAccountId;
        }

        private static string GetNinjaTraderPath()
        {
            string docs = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments);
            string ntDir = Path.Combine(docs, "NinjaTrader 8");

            if (Directory.Exists(ntDir)) return ntDir;

            string altDir = Path.Combine(
                Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
                @"NinjaTrader 8"
            );
            if (Directory.Exists(altDir)) return altDir;

            return docs;
        }

        private static string GetLicensesPath()
        {
            string ntPath = GetNinjaTraderPath();
            if (ntPath == null) return null;

            string licDir = Path.Combine(ntPath, LICENSES_SUBDIR);
            if (!Directory.Exists(licDir))
            {
                try { Directory.CreateDirectory(licDir); }
                catch { return null; }
            }
            return licDir;
        }

        public static void InvalidateCache()
        {
            _cachedAccountId = null;
            _cachedSecret = null;
        }
    }
}
