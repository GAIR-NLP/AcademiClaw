import { test, expect } from '@playwright/test'

type ScoreItem = {
  name: string
  points: number
  passed: boolean
}

const scoreItems: ScoreItem[] = []

function record(name: string, points: number, passed: boolean) {
  scoreItems.push({ name, points, passed })
}

test.afterAll(() => {
  const total = scoreItems.reduce(
    (sum, i) => sum + (i.passed ? i.points : 0),
    0
  )

  console.log('\n===== 自动评分结果 =====')
  for (const i of scoreItems) {
    console.log(
      `${i.passed ? '✅' : '❌'} ${i.name} (${i.points} 分)`
    )
  }
  console.log(`\n总分：${total} / 100`)
})

test('German Verb Notebook 功能完整性测试', async ({ page }) => {
  // 1. 首页可访问（10 分）
  try {
    await page.goto('/')
    await expect(page.getByText('自定义德语单词本')).toBeVisible()
    record('首页可访问', 10, true)
  } catch {
    record('首页可访问', 10, false)
    return
  }

  // 2. 动词入口存在并可点击（10 分）
  try {
    await page.getByRole('button', { name: '动词' }).click()
    await expect(page.getByText('动词列表')).toBeVisible()
    record('进入动词列表页', 10, true)
  } catch {
    record('进入动词列表页', 10, false)
    return
  }

  // 3. 动词列表成功加载（15 分）
  try {
    const items = page.locator('li')
    await expect(items.first()).toBeVisible()
    record('动词列表加载', 15, true)
  } catch {
    record('动词列表加载', 15, false)
  }

  // 4. 变位表可展开并显示表格（20 分）
  try {
    await page.getByText('查看变位').first().click()
    await expect(page.getByRole('table')).toBeVisible()

    // 表格结构：6 行（人称）+ 表头
    const rows = page.locator('table tbody tr')
    await expect(rows).toHaveCount(6)

    record('动词变位表展开与渲染', 20, true)
  } catch {
    record('动词变位表展开与渲染', 20, false)
  }

  // 5. 新增动词表单可用（25 分）
  try {
    await page.getByText('添加动词').click()

    await page.getByPlaceholder('动词').fill('lernen')
    await page.getByPlaceholder('中文').fill('学习')

    await page.getByText('提交').click()

    await expect(page.getByText('lernen')).toBeVisible()
    record('新增动词功能', 25, true)
  } catch {
    record('新增动词功能', 25, false)
  }

  // 6. 页面无明显运行时崩溃（20 分）
  try {
    const errors: string[] = []
    page.on('pageerror', err => errors.push(err.message))

    await page.waitForTimeout(500)
    expect(errors.length).toBe(0)

    record('无前端运行时错误', 20, true)
  } catch {
    record('无前端运行时错误', 20, false)
  }
})
