from source.manager import asset

ExpeditionReward = asset.Text(zh="探索派遣", en="Expedition Reward")
ClaimDailyCommissionReward = asset.TextTemplate(text={"zh_CN":"每日委托","en_US":"Daily Commission"})
DispatchCharacterOnExpedition = asset.TextTemplate(text={"zh_CN":"探索派遣","en_US":"Dispatch Character"})
ButtonExpeditionMD = asset.Button(threshold=0)
ButtonExpeditionLY = asset.Button(threshold=0)
ButtonExpeditionDQ = asset.Button(threshold=0)
ButtonExpeditionXM = asset.Button(threshold=0)
ButtonExpeditionClaim = asset.Button()
ButtonExpeditionFirstCharacter = asset.Button()
ButtonExpeditionSelectCharacters = asset.Button()
IconExpeditionComplete = asset.ImgIcon()
IconExpeditionComplete2 = asset.ImgIcon()
IconClaimRewardExpedition = asset.ImgIcon()
ButtonClaimBattlePathDailyMission = asset.Button(threshold=0)
ButtonSwitchToBattlePathDailyMission = asset.Button(threshold=0)
IconBattlePathExclamation = asset.ImgIcon()
ButtonExpeditionRestart = asset.Button(print_log=asset.LOG_ALL)
ButtonExpeditionClaimAll = asset.Button(print_log=asset.LOG_ALL)

ButtonCommissionUsePoints = asset.Button()
ButtonCommissionSwitchToCommissionPage = asset.Button()
IconCommissionDetailPage = asset.ImgIcon()
